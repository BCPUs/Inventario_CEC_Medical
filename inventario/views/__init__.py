from .home import home
from .usuario import user_list, user_create
from .equipo import equipo_list, equipo_create, equipo_update, equipo_delete
from .repuesto import repuesto_list, repuesto_create, repuesto_update, repuesto_delete
from .herramienta import herramienta_list, herramienta_create, herramienta_update, herramienta_delete
from .movimiento import movimiento_list, registrar_movimiento

__all__ = [
    'home',
    'user_list',
    'user_create',
    'equipo_list',
    'equipo_create',
    'equipo_update',
    'equipo_delete',
    'repuesto_list',
    'repuesto_create',
    'repuesto_update',
    'repuesto_delete',
    'herramienta_list',
    'herramienta_create',
    'herramienta_update',
    'herramienta_delete',
    'movimiento_list',
    'registrar_movimiento',
]
