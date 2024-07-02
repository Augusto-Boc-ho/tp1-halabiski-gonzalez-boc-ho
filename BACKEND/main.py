from flask import Flask, request, jsonify, render_template
from models import db, usuarios, peliculas  # Asegúrate de que estos nombres coincidan con los definidos en models.py
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://augusto:1234@localhost:5432/cameflix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def hello_world():
    return 'Hello world! ¡Dale que funcaaa!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = usuarios.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            return jsonify({"message": "Login exitoso"}), 200
        else:
            return jsonify({"message": "Credenciales inválidas"}), 401
    else:
        return render_template('login.html')

@app.route('/registrar-nuevo-usuario', methods=['POST'])  # Usamos POST para enviar datos de registro
def registrarse():
    data = request.get_json()
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    new_user = usuarios(email=email, password=password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Nuevo usuario registrado"}), 201

@app.route('/peliculas', methods=['GET'])  # Obtener todas las películas
def datos_peliculas():
    peliculas_list = peliculas.query.all()
    
    if not peliculas_list:
        return jsonify({"message": "Películas no encontradas"}), 404
    
    peliculas_data = []
    for pelicula in peliculas_list:
        peliculas_data.append({
            'titulo': pelicula.titulo,
            'descripcion': pelicula.descripcion,
            'duracion': pelicula.duracion,
            'año_creacion': pelicula.año_creacion,
            'saga': pelicula.saga,
            'link_trailer': pelicula.link_trailer,
            'link_imagen': pelicula.link_imagen
        })
    
    return jsonify(peliculas_data), 200







@app.route('/pelicula/<int:id>', methods=['GET'])  # Corrección en la definición de la ruta y método GET
def datos_pelicula(id):
    pelicula = peliculas.query.filter_by(id=id).first()
    
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

if __name__ == '__main__':
    print('Starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Server started on port ' + str(port))

    
    
# Now, let's run the backend server:
# python main.py

    

