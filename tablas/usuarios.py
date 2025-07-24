from db import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), nullable=False)
    apellido = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(300), nullable=False)
    racha = db.Column(db.Integer, default = 0, nullable = False)
    estado = db.Column(db.Boolean, default=True, nullable=False) #softdelete
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'