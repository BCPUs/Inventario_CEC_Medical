from .equipo_service import listar_equipos, obtener_equipo_por_id, registrar_equipo, eliminar_equipo
from .herramienta_service import listar_herramientas, obtener_herramienta_por_id, registrar_herramienta, eliminar_herramienta
from .repuesto_service import listar_repuestos, obtener_repuesto_por_id, registrar_repuesto, puede_eliminar_repuesto, eliminar_repuesto
from .movimiento_service import listar_movimientos, registrar_movimiento_servicio
from .usuario_service import listar_usuarios, registrar_usuario

__all__ = [
    'listar_equipos',
    'obtener_equipo_por_id',
    'registrar_equipo',
    'eliminar_equipo',
    'listar_herramientas',
    'obtener_herramienta_por_id',
    'registrar_herramienta',
    'eliminar_herramienta',
    'listar_repuestos',
    'obtener_repuesto_por_id',
    'registrar_repuesto',
    'puede_eliminar_repuesto',
    'eliminar_repuesto',
    'listar_movimientos',
    'registrar_movimiento_servicio',
    'listar_usuarios',
    'registrar_usuario',
]
