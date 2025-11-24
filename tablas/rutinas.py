from db import db

class Rutina(db.Model):
    __tablename__ = 'rutinas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    repetir = db.Column(db.String(50))
    hora = db.Column(db.Time)
    prioridad = db.Column(db.String(20))
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(255))
