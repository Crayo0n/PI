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

    # Si se envía el formulario
    if request.method == 'POST':
        datos = {
            'titulo': request.form.get('nombre', '').strip(),
            'fecha': request.form.get('fecha', '').strip(),
            'repeticion': request.form.get('repetir', '').strip(),
            'hora': request.form.get('hora', '').strip(),
            'prioridad': request.form.get('prioridad', '').strip(),
            'descripcion': request.form.get('descripcion', '').strip(),
            'rutaImagen': request.form.get('rutaImagen', '').strip()
        }

        # Validaciones por campo
        if not datos['titulo']:
            errores['titulo'] = 'El título es obligatorio'
        if not datos['fecha']:
            errores['fecha'] = 'La fecha es obligatoria'
        if not datos['repeticion']:
            errores['repeticion'] = 'Seleccione una frecuencia'
        if not datos['hora']:
            errores['hora'] = 'La hora es obligatoria'
        if not datos['prioridad']:
            errores['prioridad'] = 'Seleccione una prioridad'
        if not datos['descripcion']:
            errores['descripcion'] = 'La descripción es obligatoria'
        if not datos['rutaImagen']:
            errores['rutaImagen'] = 'Debe seleccionar una imagen'

        # Si hay errores, renderiza con datos nuevos
        if errores:
            return render_template('AcActividad.html', actividad=actividad, errores=errores, datos=datos)

        # Si no hay errores, intenta guardar cambios
        try:
            actividad.titulo = datos['titulo']
            actividad.fecha = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
            actividad.repetir = datos['repeticion']
            actividad.hora = datetime.strptime(datos['hora'], '%H:%M').time()
            actividad.prioridad = datos['prioridad']
            actividad.descripcion = datos['descripcion']
            actividad.imagen = datos['rutaImagen']

            db.session.commit()
            flash('Actividad actualizada correctamente')
            return redirect(url_for('actividades'))

        except ValueError:
            errores['fecha'] = 'Formato de fecha u hora inválido'
            return render_template('AcActividad.html', actividad=actividad, errores=errores, datos=datos)

        except SQLAlchemyError as e:
            errores['dbError'] = 'Error al guardar en la base de datos'
            db.session.rollback()
        except Exception as e:
            errores['dbError'] = 'Error inesperado al actualizar'

        return render_template('AcActividad.html', actividad=actividad, errores=errores, datos=datos)

    # Método GET: renderiza con valores actuales
    datos = {
        'titulo': actividad.titulo,
        'fecha': actividad.fecha.strftime('%Y-%m-%d'),
        'repeticion': actividad.repetir,
        'hora': actividad.hora.strftime('%H:%M'),
        'prioridad': actividad.prioridad,
        'descripcion': actividad.descripcion,
        'rutaImagen': actividad.imagen
    }

    return render_template('AcActividad.html', actividad=actividad, errores=errores, datos=datos)
