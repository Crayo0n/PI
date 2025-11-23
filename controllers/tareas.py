from flask import Blueprint, request, jsonify, session
from db import db
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios
from datetime import date

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/actualizar_tarea', methods=['POST'])
def actualizar_tarea():
    usuario_id = session.get('usuario_id')
    data = request.get_json()

    if not usuario_id or 'tarea_completada' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    tareas_id = data['tarea_completada']
    hoy = date.today()

    # Solo actualizar las tareas del día actual
    tareas_hoy = Actividades.query.filter_by(
        usuario_id=usuario_id,
        estado=True,
        fecha=hoy
    ).all()

    for tarea in tareas_hoy:
        tarea.completada = str(tarea.id) in tareas_id

    db.session.commit()

    # Verificar si todas las actividades de hoy están completadas
    todas_completadas = all(t.completada for t in tareas_hoy) and len(tareas_hoy) > 0

    usuario = Usuarios.query.get(usuario_id)

    # Solo aumentar la racha si es un nuevo día de cumplimiento
    if todas_completadas and usuario.ultima_fecha_racha != hoy:
        usuario.racha += 1
        usuario.ultima_fecha_racha = hoy
        db.session.commit()

    return jsonify({'racha': usuario.racha})
