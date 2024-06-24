import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Peliculas(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    overview = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)
    score_average = db.Column(db.Numeric(2,1))
    language = db.Column(db.String(2))
    movie_poster_link = db.Column(db.String(255))
    genres = db.Column(db.String(50))
    main_cast = db.Column(db.String(100))
    director = db.Column(db.String(30))
    trailer_link = db.Column(db.String(100))
    subtitles = db.Column(db.Boolean)
