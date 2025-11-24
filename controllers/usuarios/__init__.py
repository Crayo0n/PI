from .registrarUsuario import registrarUsuario_bp
from .actualizarUsuario import actulizarUsuario_bp
from .eliminarUsuario import eliminarUsuario_bp

usuarios_bps = [
    registrarUsuario_bp
    # actulizarUsuario_bp,
    # eliminarUsuario_bp
]

__all__ = ["usuarios_bps"]