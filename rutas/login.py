from flask import Blueprint, render_template, request, redirect, session, url_for
import tablas


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