from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
import tablas.usuarios as usuarios
from utilities import encriptarContrasena
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

registrarUsuario_bp = Blueprint('registrarUsuario', __name__)

#Registra el usuario
@registrarUsuario_bp.get('/registrarse')
def mostrarRegistrarse():
    print('Mostrando formulario de registro --------------------------------')
    errores = {}
    if session.get('usuario_id'):
        errores['userError'] = 'El usuario ya tiene una sesión abierta.'
        
    return render_template('registrarse.html', errores=errores)

@registrarUsuario_bp.route('/registrarse', methods=['POST'])
def registrarse():
    print('Intentando agregar usuario -----------------------------')
    errores = {}
    error = None

    nombre = request.form.get('Nombre', '').strip()
    apellido = request.form.get('Apellido', '').strip()
    email = request.form.get('Email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    print(f'Datos obtenidos nombre {nombre}, apellido: {apellido}, email{email}, password: {password}, confpass: {confirm_password}')
    
    match (nombre, apellido, email, password, confirm_password):
        case ('', _, _, _, _):
            errores['emptyValues'] = 'Nombre obligatorio'
        case (_, '', _, _, _):
            errores['emptyValues'] = 'Apellido obligatorio'
        case (_, _, '', _, _):
            errores['emptyValues'] = 'Email obligatorio'
        case (_, _, _, '', _):
            errores['emptyValues'] = 'Contraseña obligatoria'
        case (_, _, _, password, confirm_password) if password != confirm_password:
            errores['emptyValues'] = 'Las contraseñas no coinciden'
        case _:
            print('Error inesperado al obtener valores del formulario')
            errores['dbError'] = 'Error desconocido'

    if errores:
        print(f'Hay error en: {errores}')
        return jsonify(errores), 400 
    try:
        # Verificar si ya existe un usuario con el mismo correo
        usuario_existente = usuarios.query.filter_by(email=email).first()
        print(f'Usurio con el correo ingresado: {usuario_existente}')
        
        if usuario_existente:
            errores['userExist'] = 'Ya existe un usuario con ese correo'
            return render_template('registrarse.html', errores=errores)
        
        
        nuevo_usuario = usuarios(
            nombre=nombre,
            apellido=apellido,
            email=email,
            contrasena=encriptarContrasena.encriptar_contrasena(password),  # Usar hash para la contraseña
        )

        # Agregar a la sesión y confirmar la transacción
        db.session.add(nuevo_usuario)
        db.session.commit()

        print('Usuario agregado exitosamente.')
        flash('Usuario agregado exitosamente.')
        return render_template("login.html")

    except IntegrityError as e:
        db.session.rollback()  
        print(f'Error de integridad: {str(e.orig)}')
        errores['userExist'] = 'Ya existe un usuario con ese correo'
        return jsonify(errores), 400  # Manejar errores de duplicación de correo
    
    except Exception as e:
        db.session.rollback()  # Si ocurre cualquier otro error, revertir cambios
        print(f'Error durante la inserción: {str(e)}')
        errores['dbError'] = 'Error con la base de datos'
        return jsonify(errores), 500
    