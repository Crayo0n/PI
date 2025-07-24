from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import tablas
from decoradores import loginRequired


login_bp = Blueprint('login', __name__)

#Muestra el login
@login_bp.route("/")
def home():
    return render_template("login.html")

#Comprueba el usuario
@login_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get('email',"")
    password = request.form.get('password','')
    usuario = tablas.Usuarios.query.filter_by(email=email).first()
    if usuario and usuario.contrasena == password:
        session['usuario_id'] = usuario.id 
        return redirect(url_for('actividades')) ###3## Cambiar URL
    
    else:
        error = "Credenciales incorrectas"
        return render_template('login.html', error=error)
    

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