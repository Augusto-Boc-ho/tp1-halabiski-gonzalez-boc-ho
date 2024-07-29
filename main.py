from flask import Flask, flash, request, jsonify, render_template, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, Usuario, Pelicula, MiLista

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://valenhala:1234@localhost:5432/valentin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = 'app/static/pictures'  # Ruta donde se guardan las imágenes

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
            message = "Credenciales inválidas. Por favor, verifique su correo electrónico y contraseña."
            return render_template('login.html', message=message)

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

@app.route('/recuperar-contraseña', methods=['GET'])
def recuperar_contraseña():
    return render_template('recuperar_contraseña.html')

@app.route('/cambiar-contraseña', methods=['POST'])
def cambiar_contraseña():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    user = Usuario.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    user.contraseña = password
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/eliminar-cuenta', methods=['POST'])
def eliminar_cuenta():
    email = request.form['email']
    password = request.form['password']

    user = Usuario.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    if user.contraseña != password:
        return jsonify({"message": "Contraseña incorrecta"}), 400

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/editar_datos_usuario', methods=['GET'])
@login_required
def editar_datos_usuario():
    return render_template('editar_datos_usuario.html')

@app.route('/editar_usuario', methods=['POST'])
@login_required
def editar_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']

    if current_user.is_authenticated:
        current_user.nombre = nombre
        current_user.email = email
        if password:
            current_user.contraseña = password  # Simplemente guarda la contraseña en texto plano (no recomendado para producción)
        db.session.commit()
        flash('Tus datos han sido actualizados', 'success')
    return redirect(url_for('pagina_principal'))

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

@app.route('/peliculas/<int:id>', methods=['GET'])
def datos_pelicula(id):
    pelicula = Pelicula.query.filter_by(id=id).first()
    
    if not pelicula:
        return jsonify({"message": "Película no encontrada"}), 404
    
    return jsonify(pelicula.to_dict())

@app.route('/peliculas/<int:id>/detalle', methods=['GET'])
def detalle_pelicula(id):
    pelicula = Pelicula.query.filter_by(id=id).first()
    
    if not pelicula:
        return jsonify({"message": "Película no encontrada"}), 404
    
    return render_template('pelicula.html', pelicula=pelicula)

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

        # Verificar si la película ya está en la lista del usuario
        if MiLista.query.filter_by(id_usuario=current_user.id, id_pelicula=id_pelicula).first():
            return jsonify({"message": "La película ya está en tu lista"}), 400

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

# obtener imagen de la pelicula desde la carpeta pictures
@app.route('/pictures/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=5000)