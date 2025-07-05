from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
import tablas.actividades  


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Lista de tareas de ejemplo
tareas_importantes = [
    {"hora": "8:00 am", "descripcion": "Estudiar Física", "completada": False, "color": "azul"},
    {"hora": "10:00 am", "descripcion": "Leer", "completada": False, "color": "rosa"}
]

# Contador de racha
racha = 0
color_racha = 'default'  # Racha normal al principio

import tablas

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
        # Aquí se valida el usuario 
        usuario = tablas.Usuarios.query.filter_by(email=email).first()
        if usuario and usuario.contrasena == password:
            session['usuario_id'] = usuario.id 
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

            return redirect(url_for('login'))

        return render_template('registrarse.html', errores=errores, error=error)

    return render_template('registrarse.html', errores=errores)

@app.route('/nueva_actividad',methods=['GET', 'POST'])
def NvActividad():
    errores = {}
    if request.method == 'POST':
        titulo = request.form.get('nombre', '').strip()
        fecha = request.form.get('fecha', '').strip()
        repeticion = request.form.get('repetir', '').strip()
        hora = request.form.get('hora', '').strip()
        prioridad = request.form.get('prioridad', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        rutaImagen = request.form.get('rutaImagen', '').strip()
        
        if not titulo or not fecha or not repeticion or not hora or not prioridad or not descripcion or not rutaImagen:
            errores['empyValues'] = "Hay campos vacios"
        else:
            try:
                usuario_id = session.get('usuario_id')
                nueva_tarea = tablas.actividades(
                    titulo = titulo,
                    fecha = fecha,
                    repetir = repeticion,
                    hora = hora,
                    prioridad = prioridad,
                    descripcion = descripcion,
                    imagen = rutaImagen,
                    usuario_id=usuario_id
                )
                db.session.add(nueva_tarea)
                db.session.commit()
                flash('Actividad agregada correctamente')
                
            except Exception as e:
                errores['dbError'] = 'Error al guardar actividad'
    return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores = errores)

@app.route('/editar_actividad')
def AcActividad():
    return render_template('AcActividad.html', racha=racha, color_racha=color_racha)

    
# Ruta para manejar las actividades
@app.route('/actividades', methods=['GET', 'POST'])
def actividades():
    global racha, color_racha

    # Validar sesión
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    # Obtener actividades del usuario
    actividades_usuario = tablas.Actividades.query.filter_by(usuario_id=usuario_id).all()

    # Transformar datos a diccionarios para usar en la interfaz
    tareas_importantes = []
    for actividad in actividades_usuario:
        tareas_importantes.append({
            'id': actividad.id,
            'titulo': actividad.titulo,
            'descripcion': actividad.descripcion,
            'hora': actividad.hora.strftime('%H:%M') if actividad.hora else '',
            'imagen': actividad.imagen,
            'completada': False  # Esto se puede actualizar después si agregas un campo de estado
        })

    if request.method == 'POST':
        tarea_completada = request.form.getlist('tarea_completada')
        for idx, tarea in enumerate(tareas_importantes):
            tarea['completada'] = str(idx) in tarea_completada

        if all(tarea['completada'] for tarea in tareas_importantes):
            racha += 1
            color_racha = 'gold'
        else:
            color_racha = 'default'

        return redirect(url_for('actividades'))

    return render_template('actividades.html', tareas_importantes=tareas_importantes, racha=racha, color_racha=color_racha)

    # global racha, color_racha
    # usuario_id = session.get('usuario_id')
    # if request.method == 'POST':
    #     actividades_usuario = tablas.Actividades.query.filter_by(usuario_id=usuario_id).all()

    # # Transformar datos a diccionarios para usar en la interfaz
    #     tareas_importantes = []
    #     for actividad in actividades_usuario:
    #         tareas_importantes.append({
    #             'id': actividad.id,
    #             'titulo': actividad.titulo,
    #             'descripcion': actividad.descripcion,
    #             'hora': actividad.hora.strftime('%H:%M') if actividad.hora else '',
    #             'imagen': actividad.imagen,
    #             'completada': actividad.completada
    #         })
            
    #     tarea_completada = request.form.getlist('tarea_completada')
    #     for idx, tarea in enumerate(tareas_importantes):
    #         tarea['completada'] = str(idx) in tarea_completada
        
    #     # Verificar si todas las tareas están completadas
    #     if all(tarea['completada'] for tarea in tareas_importantes):
    #         racha += 1
    #         color_racha = 'gold'  # Cambia la racha a dorado si todas las tareas están completadas
    #     else:
    #         color_racha = 'default'

    #     return redirect(url_for('actividades'))

    # return render_template('actividades.html', tareas_importantes=tareas_importantes, racha=racha, color_racha=color_racha)

# Endpoint para manejar la actualización de las tareas
@app.route('/actualizar_tarea', methods=['POST'])
def actualizar_tarea():
    global racha, color_racha

    tarea_completada = request.json.get('tarea_completada')

    for idx, tarea in enumerate(tareas_importantes):
        tarea['completada'] = str(idx) in tarea_completada

    # Verificamos si todas las tareas están completadas y actualizamos la racha
    if all(tarea['completada'] for tarea in tareas_importantes):
        racha += 1
        color_racha = 'gold'
    else:
        color_racha = 'default'

    return jsonify({'racha': racha, 'color_racha': color_racha})


if __name__ == '__main__':
    app.run(debug=True)
