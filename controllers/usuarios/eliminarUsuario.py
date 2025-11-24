from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
from sqlalchemy.exc import SQLAlchemyError 
from flask import jsonify
from datetime import datetime
import tablas
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios


eliminarUsuario_bp = Blueprint('eliminarUsuario', __name__)

#Ya esta en eliminarUsuario

@eliminarUsuario_bp.route('/eliminar_cuenta')
def eliminar_cuenta():
    usuario = Usuarios.query.get_or_404(session['usuario_id'])
    
    try:
        db.session.delete(usuario)
        Actividades.query.filter_by(usuario_id=usuario.id).delete()
        db.session.commit()
        flash('Cuenta eliminada con éxito', 'success')
        session.pop('usuario_id', None)  # Eliminar la sesión del usuario
        return redirect(url_for('login'))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error al eliminar la cuenta', 'error')
        print(f"Error al eliminar la cuenta: {e}")
    
    return redirect(url_for('perfil'))