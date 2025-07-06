from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from db import db
from sqlalchemy.exc import SQLAlchemyError 
from flask import jsonify
from datetime import datetime
import tablas
from tablas.actividades import Actividades
from tablas.usuarios import Usuarios

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

@app.route('/nueva_actividad',methods=['GET'])
def NvActividad():
    racha = 0
    color_racha = 'default'
    errores = {}
    return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores)

@app.route('/nueva_actividad',methods=['POST'])
def PostNvActividad():
    print("Recibiendo datos de nueva actividad")
    errores = {}
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
        print(f"Datos recibidos para actividad: {titulo}, {fecha}, {repeticion}, {hora}, {prioridad}, {descripcion}, {rutaImagen}")
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            errores['fechaError'] = 'Formato de fecha incorrecto. Use YYYY-MM-DD.'
            print(f"Error de formato de fecha: {fecha}")
            return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores=errores)
        try:
            usuario_id = session.get('usuario_id')
            print(f"ID del usuario: {usuario_id}")
            nueva_tarea = tablas.Actividades(
                titulo = titulo,
                fecha = fecha_obj,
                repetir = repeticion,
                hora = hora_obj,
                prioridad = prioridad,
                descripcion = descripcion,
                imagen = rutaImagen,
                usuario_id=usuario_id
            )
            print(f"Nueva tarea creada: {nueva_tarea}")
            db.session.add(nueva_tarea)
            db.session.commit()
            flash('Actividad agregada correctamente')
            return redirect(url_for('actividades'))
        
        except SQLAlchemyError as e:
            errores['dbError'] = 'Error al guardar actividad en la base de datos'
            print(f"Error al guardar actividad en la base de datos: {e}")
            db.session.rollback()

        except Exception as e:
            print(f"Error al guardar actividad: {e}")
            errores['dbError'] = 'Error al guardar actividad'
            
    return render_template('NvActividad.html', racha=racha, color_racha=color_racha, errores = errores)

# Ruta para editar actividad
@app.route('/editar_actividad/<int:id>', methods=['GET', 'POST'])
def editar_actividad(id):
    errores = {}
    actividad = Actividades.query.get_or_404(id)

    if not actividad:
        flash('Actividad no encontrada', 'error')
        return redirect(url_for('actividades'))

    if request.method == 'POST':
        titulo = request.form.get('nombre', '').strip()
        fecha = request.form.get('fecha', '').strip()
        repeticion = request.form.get('repetir', '').strip()
        hora = request.form.get('hora', '').strip()
        prioridad = request.form.get('prioridad', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        rutaImagen = request.form.get('rutaImagen', '').strip()

        if not titulo or not fecha or not repeticion or not hora or not prioridad or not descripcion or not rutaImagen:
            errores['emptyValues'] = "Hay campos vacíos"
        else:
            try:

                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                hora_obj = datetime.strptime(hora, '%H:%M').time()
            except ValueError:
                errores['fechaError'] = 'Formato de fecha incorrecto. Use YYYY-MM-DD.'
                return render_template('editar_actividad.html', actividad=actividad, errores=errores)

            try:
                actividad.titulo = titulo
                actividad.fecha = fecha_obj
                actividad.repetir = repeticion
                actividad.hora = hora_obj
                actividad.prioridad = prioridad
                actividad.descripcion = descripcion
                actividad.imagen = rutaImagen

                db.session.commit()
                flash('Actividad actualizada correctamente')
                return redirect(url_for('actividades'))

            except SQLAlchemyError as e:
                errores['dbError'] = 'Error al actualizar la actividad en la base de datos'
                db.session.rollback() 
            except Exception as e:
                errores['dbError'] = 'Error al actualizar la actividad'
                
        return render_template('editar_actividad.html', actividad=actividad, errores=errores)

    return render_template('AcActividad.html', actividad=actividad, errores=errores)

# Ruta para eliminar actividad
@app.route('/eliminar_actividad/<int:id>')
def eliminar_actividad(id):
    actividad = Actividades.query.get_or_404(id)
    
    if not actividad:
        flash('Actividad no encontrada', 'error')
        return redirect(url_for('actividades'))

    try:
        actividad.estado = 0
        db.session.commit()
        flash('Actividad eliminada correctamente')
        return redirect(url_for('actividades'))

    except SQLAlchemyError as e:
        flash('Error al eliminar la actividad', 'error')
        db.session.rollback() 
    except Exception as e:
        flash('Error al eliminar la actividad', 'error')

    return redirect(url_for('actividades'))

# Ruta para manejar las actividades
@app.route('/actividades', methods=['GET', 'POST'])
def actividades():
    global racha, color_racha
    racha = 0
    color_racha = 'default'
    errores = {}

    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Debes iniciar sesión para continuar')
        return redirect(url_for('login'))
    try:
        # Obtener actividades del usuario
        actividades_usuario = tablas.Actividades.query.filter_by(usuario_id=usuario_id, estado=1).all()
        print(f"Actividades del usuario {usuario_id}: {actividades_usuario}")

        if not actividades_usuario:
            errores['no_actividades'] = 'Error al obtener actividades.'
            return render_template('actividades.html', tareas_importantes=[], racha=racha, color_racha=color_racha, errores=errores)

        # Transformar datos a diccionarios para usar en la interfaz
        tareas_importantes = []
        for actividad in actividades_usuario:
            tareas_importantes.append({
                'id': actividad.id,
                'titulo': actividad.titulo,
                'descripcion': actividad.descripcion,
                'hora': actividad.hora.strftime('%H:%M') if actividad.hora else '',
                'imagen': actividad.imagen,
                'completada': False  
            })
        print(f"Tareas importantes: {tareas_importantes}")
        if request.method == 'POST':
            # Procesar las tareas completadas para la racha
            tarea_completada = request.form.getlist('tarea_completada')
            for idx, tarea in enumerate(tareas_importantes):
                tarea['completada'] = str(idx) in tarea_completada

            if all(tarea['completada'] for tarea in tareas_importantes):
                racha += 1
                color_racha = 'gold'
            else:
                color_racha = 'default'

            return redirect(url_for('actividades'))
        
    except SQLAlchemyError as e:
        errores['actividades_error'] = 'Error al obtener actividades de la base de datos'
        print(f"Error al obtener actividades de la base de datos: {e}")
        tareas_importantes = []
        
    except Exception as e:
        errores['actividades_error'] = 'Error al obtener actividades'
        print(f"Error al obtener actividades: {e}")
        tareas_importantes = None

    return render_template('actividades.html', tareas_importantes=tareas_importantes, racha=racha, color_racha=color_racha, errores=errores)

    
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

@app.route('/perfil')
def perfil():
    usuario = Usuarios.query.get_or_404(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)

@app.route('/actualizar_perfil', methods=['POST'])
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

@app.route('/eliminar_cuenta')
def eliminar_cuenta():
    usuario = Usuarios.query.get_or_404(session['usuario_id'])
    
    try:
        db.session.delete(usuario)
        Actividades.query.filter_by(usuario_id=usuario.id).delete()
        db.session.commit()
        flash('Cuenta eliminada con éxito', 'success')
        session.pop('usuario_id', None)  # Eliminar la sesión del usuario
        return redirect(url_for('login'))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error al eliminar la cuenta', 'error')
        print(f"Error al eliminar la cuenta: {e}")
    
    return redirect(url_for('perfil'))


if __name__ == '__main__':
    app.run(debug=True)
