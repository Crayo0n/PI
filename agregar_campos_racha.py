from app import app
from db import db
from sqlalchemy import text

with app.app_context():
    try:
        # Ya no ejecutamos esto porque la columna ya existe:
        # db.session.execute(text('''
        #     ALTER TABLE usuarios 
        #     ADD COLUMN racha INTEGER DEFAULT 0
        # '''))

        db.session.execute(text('''
            ALTER TABLE usuarios 
            ADD COLUMN ultima_fecha_racha DATE
        '''))
        db.session.commit()
        print("✅ Columna 'ultima_fecha_racha' agregada correctamente.")
    except Exception as e:
        print("⚠️ Error al modificar la tabla usuarios:", e)
        db.session.rollback()
