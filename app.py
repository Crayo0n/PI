#Funcionales
from flask import Flask
#Base de datos
from db import db
from config import Config
#Rutas
from controllers.login import login_bp
from controllers.usuarios import usuarios_bps
from controllers.actividades import actividades_bps
from controllers.rutinas import rutinas_bp
from controllers.tareas import tareas_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

# Rutas -------------------------

app.register_blueprint(login_bp)
app.register_blueprint(rutinas_bp)
app.register_blueprint(tareas_bp)

for bp in usuarios_bps + actividades_bps:
    app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)


