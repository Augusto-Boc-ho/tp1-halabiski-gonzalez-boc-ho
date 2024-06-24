from flask import Flask, request, jsonify
from models import db, Peliculas
from flask_cors import CORS

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://tomi:123456789@localhost:5432/peliculas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
CORS(app)
db.init_app(app)

@app.route('/')
def home():
    return "hello world!"

@app.route('/peliculas')
def ver_peliculas():
    try:
        Peliculas_total = Peliculas.query.all()
        Peliculas_data = []
        for Pelicula in Peliculas_total:
            Pelicula_data = {
                "id": Pelicula.id,
                "title": Pelicula.title,
                "overview": Pelicula.overview,
                "release_date": Pelicula.release_date,
                "score_average": Pelicula.score_average,
                "language": Pelicula.language,
                "movie_poster_link": Pelicula.movie_poster_link,
                "genres": Pelicula.genres,
                "main_cast": Pelicula.main_cast,
                "director": Pelicula.director,
                "trailer_link": Pelicula.trailer_link,
                "subtitles": Pelicula.subtitles,
            }
            Peliculas_data.append(Pelicula_data)
            return jsonify(Peliculas_data)
    except:
        return jsonify({"Error"})


@app.route('/peliculas/<id>')
def data(id):
    Pelicula = Peliculas.query.get(id)
    try:
        Pelicula_data = {
            "id": Pelicula.id,
            "title": Pelicula.title,
            "overview": Pelicula.overview,
            "release_date": Pelicula.release_date,
            "score_average": Pelicula.score_average,
            "language": Pelicula.language,
            "movie_poster_link": Pelicula.movie_poster_link,
            "genres": Pelicula.genres,
            "main_cast": Pelicula.main_cast,
            "director": Pelicula.director,
            "trailer_link": Pelicula.trailer_link,
            "subtitles": Pelicula.subtitles,
        }
        return jsonify(Pelicula_data)
    except:
        return jsonify({"mensaje": "La pelicula no existe."})

if __name__ == '__main__':
    print('starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')
