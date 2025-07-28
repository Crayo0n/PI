from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import tablas
from decoradores import loginRequired
from utilities import encriptarContrasena

login_bp = Blueprint('login', __name__)

#Muestra el login
@login_bp.route("/")
def home():
    return render_template("login.html")

#Comprueba el usuario
@login_bp.route("/login", methods=["POST"])
def login():
    print('Iniciando sesion ----------------')
    errores = {}
    email = request.form.get('email',"")
    password = request.form.get('password','')
    print(f'Datos obtenidos: {email} y {password}')
    if not password or not email:
        errores['emptyValues'] = 'Ingrese todos los campos'
    else:
        usuario = tablas.Usuarios.query.filter_by(email=email).first()
        if usuario:
            resultado = encriptarContrasena.verificar_contrasena(password,usuario.contrasena)
            if resultado:
                print('Ingresando a lista de actividades ----------------------')
                session['usuario_id'] = usuario.id 
                return render_template('actividades.html', errores = errores) ###3## Cambiar URL
            else:
                errores['passwordError'] = 'La contraseña es incorrecta'
        else:
            errores['userError'] = 'No hay usuario con ese correo registrado'
            
    return render_template('login.html', errores=errores)
    

#Cierre de sesion
@loginRequired
@login_bp.route("cerrarSesion")
def cerrarSesion():
    print("Entrando a cerrar sesión ------------------")
    try:
        session.clear()  
        flash("Sesión cerrada correctamente.")
        return redirect(url_for("login.home"))
    except Exception as e:
        errores = {}
        errores["sessionError"] = "Error al cerrar sesión"
        print(f"Error al cerrar sesión: {str(e)}")
        return render_template("login.html", err=errores)