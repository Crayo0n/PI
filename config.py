class Config:
    #BD configuraciones
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Clave secreta
    SECRET_KEY = 'mysecretkey'
