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
        return redirect(url_for('actividades'))

    try:
        actividad.estado = 0
        db.session.commit()
        flash('Actividad eliminada correctamente')
        return redirect(url_for('actividades'))

    except SQLAlchemyError as e:
        flash('Error al eliminar la actividad', 'error')
        db.session.rollback() 
    except Exception as e:
        flash('Error al eliminar la actividad', 'error')

    return redirect(url_for('actividades'))