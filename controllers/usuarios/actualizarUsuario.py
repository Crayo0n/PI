from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
from sqlalchemy.exc import SQLAlchemyError 
from flask import jsonify
from datetime import datetime
import tablas
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios

actulizarUsuario_bp = Blueprint('actulizarUsuario', __name__)

#Ya esta en actualizar Usuario
@actulizarUsuario_bp.route('/perfil')
def perfil():
    usuario = Usuarios.query.get_or_404(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)
#Ya esta en actualizar perfil
@actulizarUsuario_bp.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    usuario = Usuarios.query.get_or_404(session['usuario_id'])
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    contrasena = request.form.get('contrasena', '').strip()
    confirmar_contrasena = request.form.get('confirmar_contrasena', '').strip()
    email = request.form.get('email', '').strip()

    if contrasena != confirmar_contrasena:
        flash('Las contraseñas no coinciden', 'error')

    # Validar y actualizar los datos del usuario
    if nombre and apellido and contrasena and email:
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.contrasena = contrasena
        usuario.email = email
        db.session.commit()
        flash('Perfil actualizado con éxito')
    else:
        flash('Por favor, completa todos los campos')

    return redirect(url_for('perfil'))