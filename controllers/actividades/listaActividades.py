from flask import Blueprint, render_template, request, redirect, session, url_for, flash, jsonify
import tablas
from sqlalchemy.exc import SQLAlchemyError 
from decoradores import loginRequired

listaActividades_bp = Blueprint('listaActividades', __name__)

# Ruta para manejar las actividades
@listaActividades_bp.route('/actividades', methods=['GET', 'POST'])
def actividades():
    global racha, color_racha
    racha = 0
    color_racha = 'default'
    errores = {}

    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Debes iniciar sesión para continuar')
        return redirect(url_for('login'))
    try:
        # Obtener actividades del usuario
        actividades_usuario = tablas.Actividades.query.filter_by(usuario_id=usuario_id, estado=1).all()
        print(f"Actividades del usuario {usuario_id}: {actividades_usuario}")

        if not actividades_usuario:
            errores['no_actividades'] = 'Error al obtener actividades.'
            return render_template(
                'actividades.html',
                tareas_importantes=[],
                racha=racha,
                color_racha=color_racha,
                errores=errores
            )

        # Transformar datos a diccionarios para usar en la interfaz
        tareas_importantes = []
        for actividad in actividades_usuario:
            tareas_importantes.append({
                'id': actividad.id,
                'titulo': actividad.titulo,
                'descripcion': actividad.descripcion,
                'prioridad': actividad.prioridad,
                'hora': actividad.hora.strftime('%H:%M') if actividad.hora else '',
                'imagen': actividad.imagen,
                'completada': bool(actividad.completada)  # <- se usa lo que hay en BD
            })
        print(f"Tareas importantes: {tareas_importantes}")

        if request.method == 'POST':
            # Procesar las tareas completadas para la racha (lógica antigua por formulario)
            tarea_completada = request.form.getlist('tarea_completada')
            for idx, tarea in enumerate(tareas_importantes):
                tarea['completada'] = str(idx) in tarea_completada

            if all(tarea['completada'] for tarea in tareas_importantes):
                racha += 1
                color_racha = 'gold'
            else:
                color_racha = 'default'

            return redirect(url_for('actividades'))
        
    except SQLAlchemyError as e:
        errores['actividades_error'] = 'Error al obtener actividades de la base de datos'
        print(f"Error al obtener actividades de la base de datos: {e}")
        tareas_importantes = []
        
    except Exception as e:
        errores['actividades_error'] = 'Error al obtener actividades'
        print(f"Error al obtener actividades: {e}")
        tareas_importantes = None

    return render_template(
        'actividades.html',
        tareas_importantes=tareas_importantes,
        racha=racha,
        color_racha=color_racha,
        errores=errores
    )


# NUEVA RUTA para manejar el fetch('/actualizar_tarea', ...) del checkbox
@listaActividades_bp.route('/actualizar_tarea', methods=['POST'])
def actualizar_tarea():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401

    try:
        data = request.get_json(silent=True) or {}
        ids_recibidos = data.get('tarea_completada', [])

        # Normalizar a lista de enteros
        ids_int = []
        if isinstance(ids_recibidos, list):
            for valor in ids_recibidos:
                try:
                    ids_int.append(int(valor))
                except (ValueError, TypeError):
                    continue

        # Obtener actividades del usuario
        actividades_usuario = tablas.Actividades.query.filter_by(
            usuario_id=usuario_id,
            estado=1
        ).all()

        # Actualizar campo "completada" según lo que venga marcado
        for actividad in actividades_usuario:
            actividad.completada = actividad.id in ids_int

        # Guardar cambios
        tablas.db.session.commit()

        # Calcular una racha simple: 1 si todas las tareas del día están completadas, 0 si no
        if actividades_usuario and all(a.completada for a in actividades_usuario):
            racha_valor = 1
        else:
            racha_valor = 0

        return jsonify({'success': True, 'racha': racha_valor})

    except Exception as e:
        tablas.db.session.rollback()
        print(f"Error al actualizar tareas: {e}")
        return jsonify({'success': False, 'error': 'Error al actualizar tareas'}), 500