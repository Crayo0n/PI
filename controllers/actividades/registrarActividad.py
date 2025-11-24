from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
from sqlalchemy.exc import SQLAlchemyError 
from flask import jsonify
from datetime import datetime
import tablas
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios

# Contador de racha
racha = 0
color_racha = 'default'  # Racha normal al principio

registrarActividad_bp = Blueprint('registrarActividad', __name__)

@registrarActividad_bp.route('/nueva_actividad',methods=['GET'])
def NvActividad():
    racha = 0
    color_racha = 'default'
    errores = {}
    datos = {}
    return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores, datos=datos)

@registrarActividad_bp.route('/nueva_actividad', methods=['POST'])
def PostNvActividad():
    errores = {}
    datos = {}  # <- aquí guardaremos los datos del formulario

    # Obtener valores del formulario
    datos['titulo'] = request.form.get('nombre', '').strip()
    datos['fecha'] = request.form.get('fecha', '').strip()
    datos['repeticion'] = request.form.get('repetir', '').strip()
    datos['hora'] = request.form.get('hora', '').strip()
    datos['prioridad'] = request.form.get('prioridad', '').strip()
    datos['descripcion'] = request.form.get('descripcion', '').strip()
    datos['rutaImagen'] = request.form.get('rutaImagen', '').strip()

    # Validaciones por campo
    if not datos['titulo']:
        errores['titulo'] = 'El título es obligatorio'
    if not datos['fecha']:
        errores['fecha'] = 'La fecha es obligatoria'
    if not datos['repeticion']:
        errores['repeticion'] = 'Debe seleccionar una frecuencia de repetición'
    if not datos['hora']:
        errores['hora'] = 'La hora es obligatoria'
    if not datos['prioridad']:
        errores['prioridad'] = 'Debe seleccionar una prioridad'
    if not datos['descripcion']:
        errores['descripcion'] = 'La descripción es obligatoria'
    if not datos['rutaImagen']:
        errores['rutaImagen'] = 'Debe seleccionar una imagen'

    # Si hay errores, renderizamos con los datos ingresados
    if errores:
        print("Errores detectados:", errores)
        return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores, datos=datos)

    try:
        fecha_obj = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
        hora_obj = datetime.strptime(datos['hora'], '%H:%M').time()
    except ValueError:
        errores['fecha'] = 'Formato de fecha u hora incorrecto'
        print(f"Error de formato: fecha={datos['fecha']}, hora={datos['hora']}")
        return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores, datos=datos)

    try:
        usuario_id = session.get('usuario_id')
        nueva_tarea = tablas.Actividades(
            titulo=datos['titulo'],
            fecha=fecha_obj,
            repetir=datos['repeticion'],
            hora=hora_obj,
            prioridad=datos['prioridad'],
            descripcion=datos['descripcion'],
            imagen=datos['rutaImagen'],
            usuario_id=usuario_id
        )
        db.session.add(nueva_tarea)
        db.session.commit()
        flash('Actividad agregada correctamente')
        return redirect(url_for('listaActividades.actividades'))

    except SQLAlchemyError as e:
        errores['dbError'] = 'Error al guardar en la base de datos'
        print("Error SQL:", e)
        db.session.rollback()

    return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores, datos=datos)
