from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

import tablas
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios


actulizarUsuario_bp = Blueprint('actulizarUsuario', __name__)


@actulizarUsuario_bp.route('/perfil')
def perfil():
    # Obtener el usuario en sesión
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Debes iniciar sesión para continuar', 'error')
        # Ajusta el endpoint de login según tu proyecto
        return redirect(url_for('login.home') if 'login.home' in url_for.__globals__ else url_for('login'))

    usuario = Usuarios.query.get_or_404(usuario_id)
    return render_template('perfil.html', usuario=usuario)


@actulizarUsuario_bp.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Debes iniciar sesión para continuar', 'error')
        return redirect(url_for('login.home') if 'login.home' in url_for.__globals__ else url_for('login'))

    usuario = Usuarios.query.get_or_404(usuario_id)

    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    contrasena = request.form.get('contrasena', '').strip()
    confirmar_contrasena = request.form.get('confirmar_contrasena', '').strip()
    email = request.form.get('email', '').strip()


    if contrasena != confirmar_contrasena:
        flash('Las contraseñas no coinciden', 'error')
        return redirect(url_for('actulizarUsuario.perfil'))


    if nombre and apellido and contrasena and email:
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.contrasena = contrasena
        usuario.email = email
        db.session.commit()
        flash('Perfil actualizado con éxito', 'success')
    else:
        flash('Por favor, completa todos los campos', 'error')


    return redirect(url_for('actulizarUsuario.perfil'))