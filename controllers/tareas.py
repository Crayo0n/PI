from flask import Blueprint, request, jsonify, session
from db import db
from datetime import datetime
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios

tareas_bp = Blueprint('tareas', __name__)

from flask import Blueprint, request, jsonify, session
from db import db
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios
from datetime import date

actualizar_tarea_bp = Blueprint('actualizar_tarea', __name__)

@actualizar_tarea_bp.route('/actualizar_tarea', methods=['POST'])
def actualizar_tarea():
    usuario_id = session.get('usuario_id')
    data = request.get_json()

    if not usuario_id or 'tarea_completada' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    tareas_id = data['tarea_completada']

    # Marcar tareas completadas según el checkbox
    tareas_usuario = Actividades.query.filter_by(usuario_id=usuario_id, estado=True).all()
    for tarea in tareas_usuario:
        tarea.completada = str(tarea.id) in tareas_id

    db.session.commit()

    # Evaluar si todas las actividades del día actual están completadas
    hoy = date.today()
    tareas_hoy = Actividades.query.filter_by(
        usuario_id=usuario_id,
        estado=True,
        fecha=hoy
    ).all()

    todas_completadas = all(t.completada for t in tareas_hoy) and len(tareas_hoy) > 0

    usuario = Usuarios.query.get(usuario_id)

    # Aumentar racha solo si no se ha registrado aún (p. ej., no aumentar varias veces en el mismo día)
    if todas_completadas and usuario.ultima_fecha_racha != hoy:
        usuario.racha += 1
        usuario.ultima_fecha_racha = hoy
        db.session.commit()

    return jsonify({'racha': usuario.racha})

