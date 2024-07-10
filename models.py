from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    año_creacion = db.Column(db.Integer, nullable=False)
    saga = db.Column(db.String(255), nullable=False)
    link_trailer = db.Column(db.String(255), nullable=False)
    link_imagen = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'duracion': self.duracion,
            'año_creacion': self.año_creacion,
            'saga': self.saga,
            'link_trailer': self.link_trailer,
            'link_imagen': self.link_imagen,
            'fecha_creacion': self.fecha_creacion
        }

class MiLista(db.Model):
    __tablename__ = 'mi_lista'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id_pelicula = db.Column(db.Integer, db.ForeignKey('peliculas.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())
