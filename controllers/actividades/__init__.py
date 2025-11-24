from .registrarActividad import registrarActividad_bp
from .editarActividad import editarActividad_bp
from .eliminarActividad import eliminarActividad_bp
from .listaActividades import listaActividades_bp

actividades_bps = [
    listaActividades_bp,
    registrarActividad_bp,
    editarActividad_bp,
    eliminarActividad_bp
]

__all__ = ["actividades_bps"]