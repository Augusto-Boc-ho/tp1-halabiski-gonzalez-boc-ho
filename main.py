import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, Usuario, Pelicula, MiLista

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://augusto:1234@localhost:5432/cameflix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.query.filter_by(email=email).first()

        if user and user.contraseña == password:
            login_user(user)
            return redirect(url_for('pagina_principal'))
        else:
            return jsonify({"message": "Credenciales inválidas"}), 401

    return render_template('login.html')

@app.route('/registrar-nuevo-usuario', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if Usuario.query.filter_by(email=email).first():
            return jsonify({"message": "El email ya está registrado"}), 400

        new_user = Usuario(nombre=nombre, email=email, contraseña=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('registrar_nuevo_usuario.html')

@app.route('/pagina_principal')
@login_required
def pagina_principal():
    return render_template('principal.html', nombre=current_user.nombre)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    lista_peliculas = Pelicula.query.all()
    peliculas_json = [pelicula.to_dict() for pelicula in lista_peliculas]
    return jsonify(peliculas_json)

@app.route('/pelicula/<int:id>', methods=['GET'])
def datos_pelicula(id):
    pelicula = Pelicula.query.filter_by(id=id).first()
    
    if not pelicula:
        return jsonify({"message": "Película no encontrada"}), 404
    
    return jsonify({
        'titulo': pelicula.titulo,
        'descripcion': pelicula.descripcion,
        'duracion': pelicula.duracion,
        'año_creacion': pelicula.año_creacion,
        'saga': pelicula.saga,
        'link_trailer': pelicula.link_trailer,
        'link_imagen': pelicula.link_imagen
    }), 200
    

@app.route('/mi-lista', methods=['GET'])
@login_required
def obtener_lista_usuario():
    mi_lista = MiLista.query.filter_by(id_usuario=current_user.id).all()
    peliculas = [Pelicula.query.filter_by(id=entry.id_pelicula).first().to_dict() for entry in mi_lista]
    return jsonify(peliculas), 200


@app.route('/agregar-pelicula', methods=['POST'])
@login_required
def agregar_pelicula():
    try:
        id_pelicula = request.json.get('id_pelicula')
        pelicula = Pelicula.query.filter_by(id=id_pelicula).first()

        if not pelicula:
            return jsonify({"message": "Película no encontrada"}), 404

        nueva_pelicula = MiLista(id_usuario=current_user.id, id_pelicula=id_pelicula)
        db.session.add(nueva_pelicula)
        db.session.commit()

        return jsonify(pelicula.to_dict()), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal server error"}), 500

@app.route('/eliminar-pelicula', methods=['POST'])
@login_required
def eliminar_pelicula():
    id_pelicula = request.json.get('id_pelicula')
    pelicula = MiLista.query.filter_by(id_usuario=current_user.id, id_pelicula=id_pelicula).first()

    if not pelicula:
        return jsonify({"message": "Película no encontrada en la lista"}), 404

    db.session.delete(pelicula)
    db.session.commit()

    return jsonify({"id": id_pelicula}), 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=5000)
