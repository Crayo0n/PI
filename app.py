#Funcionales
from flask import Flask
#Base de datos
from db import db
from config import Config
#Rutas
from rutas.login import login_bp                #inicio de sesión
from rutas.usuarios import usuarios_bps         #rutas de usuarios
from rutas.actividades import actividades_bps   #rutas de actividades


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

# Rutas -------------------------

#Inicio de sesion
app.register_blueprint(login_bp)

#Rutas de la aplicacion
for bp in usuarios_bps + actividades_bps:
    app.register_blueprint(bp)



if __name__ == '__main__':
    app.run(debug=True)
