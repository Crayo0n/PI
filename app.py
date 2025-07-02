from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Aquí validas el usuario (esto es solo un ejemplo básico)
        if email == "admin@correo.com" and password == "1234":
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
            # Aquí guardarías al usuario (simulación de registro)
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('login'))

        return render_template('registrarse.html', errores=errores, error=error)

    return render_template('registrarse.html', errores=errores)


# Ruta para manejar las actividades
@app.route('/actividades', methods=['GET', 'POST'])
def actividades():
    global racha, color_racha

    if request.method == 'POST':
        tarea_completada = request.form.getlist('tarea_completada')

        for idx, tarea in enumerate(tareas_importantes):
            if str(idx) in tarea_completada:
                tareas_importantes[idx]['completada'] = True
            else:
                tareas_importantes[idx]['completada'] = False

        # Verificar si todas las tareas están completadas
        if all(tarea['completada'] for tarea in tareas_importantes):
            racha += 1
            color_racha = 'gold'  # Cambia la racha a dorado si todas las tareas están completadas
        else:
            color_racha = 'default'

        return redirect(url_for('actividades'))

    return render_template('actividades.html', tareas_importantes=tareas_importantes, racha=racha, color_racha=color_racha)

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
