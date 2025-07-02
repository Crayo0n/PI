from flask import Flask, render_template, request, redirect, url_for
from db import db  
import tablas
app = Flask(__name__)
# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.before_request
def create_tables():
    db.create_all()
# Rutas de la aplicación
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Aquí validas el usuario 
        usuario = tablas.Usuarios.query.filter_by(email=email).first()
        if usuario and usuario.contrasena == password:
            return redirect(url_for('actividades'))
        else:
            error = "Credenciales incorrectas"
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/registrarse', methods=['GET', 'POST'])
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
            # Aquí se guarda el usuario en la base de datos
            nuevo_usuario = tablas.Usuarios(
                nombre=nombre,
                apellido=apellido,
                email=email,
                contrasena=password
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            return redirect(url_for('login'))

        return render_template('registrarse.html', errores=errores, error=error)

    return render_template('registrarse.html', errores=errores)




@app.route('/actividades',  methods=['POST'])
def actividades():
    tareas_importantes = [
        {"hora": "8:00 am", "descripcion": "Estudiar Física", "color": "azul", "completada": False},
        {"hora": "10:00 am", "descripcion": "Leer", "color": "rosa", "completada": True}
    ]
    return render_template('actividades.html', tareas_importantes=tareas_importantes)


if __name__ == '__main__':
    app.run(debug=True)
