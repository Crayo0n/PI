from db import db

class Actividades(db.Model):
    __tablename__ = 'actividades'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=True)
    repetir = db.Column(db.String(20), nullable=True)  # diario, semanal, mensual
    hora = db.Column(db.Time, nullable=True)
    prioridad = db.Column(db.String(10), nullable=True)  # alta, media, baja
    descripcion = db.Column(db.Text, nullable=True)
    imagen = db.Column(db.String(200), nullable=True)  # ruta a la imagen
    completada = db.Column(db.Boolean, default=False, nullable=False)
    estado = db.Column(db.Integer, default=1, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuarios', backref='actividades')
