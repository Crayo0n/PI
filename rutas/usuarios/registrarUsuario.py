from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
import tablas


registrarUsuario_bp = Blueprint('registrarUsuario', __name__)

#Registra el usuario
@registrarUsuario_bp.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    errores = {}
    error = None

    if request.method == 'POST':
        nombre = request.form.get('Nombre', '').strip()
        apellido = request.form.get('Apellido', '').strip()
        email = request.form.get('Email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validaciones
        if not nombre:
            errores['Nombre'] = 'Nombre obligatorio'
        if not apellido:
            errores['Apellido'] = 'Apellido obligatorio'
        if not email:
            errores['Email'] = 'Email obligatorio'
        if password != confirm_password:
            error = 'Las contraseñas no coinciden'

        if not errores and not error:
            flash('Usuario registrado correctamente', 'success')
            # Aquí se guarda el usuario en la base de datos
            nuevo_usuario = tablas.Usuarios(
                nombre=nombre,
                apellido=apellido,
                email=email,
                contrasena=password
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            return redirect(url_for('login.home'))

        return render_template('registrarse.html', errores=errores, error=error)

    return render_template('registrarse.html', errores=errores)