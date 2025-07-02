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




# Lista de tareas de ejemplo
tareas_importantes = [
    {"hora": "8:00 am", "descripcion": "Estudiar Física", "completada": False, "color": "azul"},
    {"hora": "10:00 am", "descripcion": "Leer", "completada": False, "color": "rosa"}
]

# Contador de racha
racha = 0
color_racha = 'default'  # Racha normal al principio

@app.route('/actividades', methods=['GET', 'POST'])
def actividades():
    global racha, color_racha
    
    if request.method == 'POST':
        tarea_completada = request.form.getlist('tarea_completada')  # Lista de índices de las tareas completadas
        
        # Marca las tareas como completadas según los checkboxes seleccionados
        for idx, tarea in enumerate(tareas_importantes):
            if str(idx) in tarea_completada:
                tareas_importantes[idx]['completada'] = True
            else:
                tareas_importantes[idx]['completada'] = False
        
        # Verifica si todas las tareas fueron completadas
        if all(tarea['completada'] for tarea in tareas_importantes):
            racha += 1
            color_racha = 'gold'  # Cambia el color de la racha a dorado si todas las tareas están completas
        else:
            color_racha = 'default'  # Racha normal
        
        return redirect(url_for('actividades'))

    return render_template('actividades.html', tareas_con_indice=enumerate(tareas_importantes), racha=racha, color_racha=color_racha)


if __name__ == '__main__':
    app.run(debug=True)
