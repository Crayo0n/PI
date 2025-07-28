from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
from sqlalchemy.exc import SQLAlchemyError 
from flask import jsonify
from datetime import datetime
import tablas
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios

editarActividad_bp = Blueprint('editarActividad', __name__)

@editarActividad_bp.route('/editar_actividad/<int:id>', methods=['GET', 'POST'])
def editar_actividad(id):
    errores = {}
    actividad = Actividades.query.get_or_404(id)

    if not actividad:
        flash('Actividad no encontrada', 'error')
        return redirect(url_for('actividades'))

    if request.method == 'POST':
        titulo = request.form.get('nombre', '').strip()
        fecha = request.form.get('fecha', '').strip()
        repeticion = request.form.get('repetir', '').strip()
        hora = request.form.get('hora', '').strip()
        prioridad = request.form.get('prioridad', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        rutaImagen = request.form.get('rutaImagen', '').strip()

        if not titulo or not fecha or not repeticion or not hora or not prioridad or not descripcion or not rutaImagen:
            errores['emptyValues'] = "Hay campos vacíos"
        else:
            try:

                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                hora_obj = datetime.strptime(hora, '%H:%M').time()
            except ValueError:
                errores['fechaError'] = 'Formato de fecha incorrecto. Use YYYY-MM-DD.'
                return render_template('editar_actividad.html', actividad=actividad, errores=errores)

            try:
                actividad.titulo = titulo
                actividad.fecha = fecha_obj
                actividad.repetir = repeticion
                actividad.hora = hora_obj
                actividad.prioridad = prioridad
                actividad.descripcion = descripcion
                actividad.imagen = rutaImagen

                db.session.commit()
                flash('Actividad actualizada correctamente')
                return redirect(url_for('actividades'))

            except SQLAlchemyError as e:
                errores['dbError'] = 'Error al actualizar la actividad en la base de datos'
                db.session.rollback() 
            except Exception as e:
                errores['dbError'] = 'Error al actualizar la actividad'
                
        return render_template('editar_actividad.html', actividad=actividad, errores=errores)

    return render_template('AcActividad.html', actividad=actividad, errores=errores)