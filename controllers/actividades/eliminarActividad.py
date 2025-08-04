from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
from sqlalchemy.exc import SQLAlchemyError 
from flask import jsonify
from datetime import datetime
import tablas
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios

eliminarActividad_bp = Blueprint('eliminarActividad', __name__)

@eliminarActividad_bp.route('/eliminar_actividad/<int:id>')
def eliminar_actividad(id):
    actividad = Actividades.query.get_or_404(id)
    
    if not actividad:
        flash('Actividad no encontrada', 'error')
        return redirect(url_for('listaActividades.actividades'))

    try:
        actividad.estado = 0
        db.session.commit()  # 👈 Si esto falla, no se muestra el mensaje de éxito
        flash('Actividad eliminada correctamente', 'success')
        return redirect(url_for('listaActividades.actividades'))

    except SQLAlchemyError as e:
        db.session.rollback() 
        flash('Error al eliminar la actividad (base de datos)', 'error')

    except Exception as e:
        flash('Error inesperado al eliminar la actividad', 'error')

    return redirect(url_for('listaActividades.actividades'))
