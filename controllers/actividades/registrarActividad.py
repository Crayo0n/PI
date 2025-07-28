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
    return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores)

@registrarActividad_bp.route('/nueva_actividad',methods=['POST'])
def PostNvActividad():
    print("Recibiendo datos de nueva actividad")
    errores = {}
    titulo = request.form.get('nombre', '').strip()
    fecha = request.form.get('fecha', '').strip()
    repeticion = request.form.get('repetir', '').strip()
    hora = request.form.get('hora', '').strip()
    prioridad = request.form.get('prioridad', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    rutaImagen = request.form.get('rutaImagen', '').strip()
        
    if not titulo or not fecha or not repeticion or not hora or not prioridad or not descripcion or not rutaImagen:
        errores['empyValues'] = "Hay campos vacios"
    else:
        print(f"Datos recibidos para actividad: {titulo}, {fecha}, {repeticion}, {hora}, {prioridad}, {descripcion}, {rutaImagen}")
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            errores['fechaError'] = 'Formato de fecha incorrecto. Use YYYY-MM-DD.'
            print(f"Error de formato de fecha: {fecha}")
            return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores)
        try:
            usuario_id = session.get('usuario_id')
            print(f"ID del usuario: {usuario_id}")
            nueva_tarea = tablas.Actividades(
                titulo = titulo,
                fecha = fecha_obj,
                repetir = repeticion,
                hora = hora_obj,
                prioridad = prioridad,
                descripcion = descripcion,
                imagen = rutaImagen,
                usuario_id=usuario_id
            )
            print(f"Nueva tarea creada: {nueva_tarea}")
            db.session.add(nueva_tarea)
            db.session.commit()
            flash('Actividad agregada correctamente')
            return redirect(url_for('actividades'))
        
        except SQLAlchemyError as e:
            errores['dbError'] = 'Error al guardar actividad en la base de datos'
            print(f"Error al guardar actividad en la base de datos: {e}")
            db.session.rollback()

        except Exception as e:
            print(f"Error al guardar actividad: {e}")
            errores['dbError'] = 'Error al guardar actividad'
            
    return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores = errores)