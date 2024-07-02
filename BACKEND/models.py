import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False) #nullable=False significa que no puede ser nulo lo que inserte en ese campo
    email = db.Column(db.String(255), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())
    
class peliculas(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    año_creacion = db.Column(db.Integer, nullable=False)
    saga = db.Column(db.String(255), nullable=False)
    link_trailer = db.Column(db.String(255), nullable=False)
    link_imagen = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())
    
class mi_lista(db.Model):
    __tablename__ = 'mi_lista'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id_pelicula = db.Column(db.Integer, db.ForeignKey('peliculas.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())
    