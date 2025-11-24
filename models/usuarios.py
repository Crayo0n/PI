from db import db
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

def agregarUsuario(nuevoUsuario):
    errores = {}
    try:
        db.session.add(nuevoUsuario)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()  
        print(f'Error de integridad: {str(e.orig)}')
        errores['dbError'] = 'Error 0 durante la insersion de usuarios'
    except OperationalError as e:
        db.session.rollback()
        print(f'Error de operacion de la base de datos: {str(e.orig)}')
        errores['dbError'] = 'Error 1 durante el insersion de usuarios'
    except Exception as e:
        db.session.rollback()  # Si ocurre cualquier otro error, revertir cambios
        print(f'Error durante la inserción: {str(e)}')
        errores['dbError'] = 'Error 2 durante la insersiond e usuarios'

    return errores