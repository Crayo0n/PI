from app import app  
from db import db
from tablas.rutinas import Rutina
from datetime import time

with app.app_context():
    nueva_rutina = Rutina(
        titulo='Ejercicio Matutino',
        repetir='diario',
        hora=time(7, 0),
        prioridad='alta',
        descripcion='15 minutos de estiramiento y cardio suave',
        imagen='static/img/imagen2.png'
    )
    db.session.add(nueva_rutina)
    db.session.commit()
    print("✅ Rutina insertada correctamente.")
