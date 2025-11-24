from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import db
from tablas.rutinas import Rutina
from tablas.actividades import Actividades
from datetime import datetime

rutinas_bp = Blueprint('rutinas', __name__, url_prefix='/rutinas')


@rutinas_bp.route('/')
def mostrar_rutinas():
    rutinas = Rutina.query.all()
    return render_template('rutinas.html', rutinas=rutinas)


@rutinas_bp.route('/agregar/<int:id>', methods=['POST'])
def agregar_rutina(id):
    rutina = Rutina.query.get_or_404(id)
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        flash('Debes iniciar sesión para agregar una rutina', 'error')
        return redirect(url_for('login'))

    try:
        nueva_actividad = Actividades(
            titulo=rutina.titulo,
            fecha=datetime.today().date(),  # Puedes permitir personalizar
            repetir=rutina.repetir,
            hora=rutina.hora,
            prioridad=rutina.prioridad,
            descripcion=rutina.descripcion,
            imagen=rutina.imagen,
            usuario_id=usuario_id
        )
        db.session.add(nueva_actividad)
        db.session.commit()
        flash('Rutina agregada a tus actividades', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar rutina', 'error')

    return redirect(url_for('rutinas.mostrar_rutinas'))
