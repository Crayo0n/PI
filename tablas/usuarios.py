from db import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), nullable=False)
    apellido = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    activo = db.Column(db.Integer, default=1, nullable=False)
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'