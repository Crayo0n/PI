from app import app  
from db import db
from tablas.rutinas import Rutina
from datetime import time

with app.app_context():
    rutinas = [
        Rutina(
            titulo='Rutina de Concentración',
            repetir='diario',
            hora=time(9, 0),
            prioridad='media',
            descripcion='Sesión de trabajo profundo sin interrupciones durante 50 minutos',
            imagen='static/img/imagen3.png'
        ),
        Rutina(
            titulo='Pausa Activa',
            repetir='diario',
            hora=time(11, 30),
            prioridad='baja',
            descripcion='5 minutos de caminata y estiramientos para recargar energía',
            imagen='static/img/imagen4.png'
        ),
        Rutina(
            titulo='Lectura Nocturna',
            repetir='diario',
            hora=time(21, 0),
            prioridad='media',
            descripcion='Leer 20 minutos antes de dormir sin distracciones electrónicas',
            imagen='static/img/imagen5.png'
        )
    ]

    db.session.add_all(rutinas)
    db.session.commit()
    print("✅ Rutinas insertadas correctamente.")
