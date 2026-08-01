from django.contrib import admin
from inventario.models.equipo import EquipoMedico
from inventario.models.repuesto import Repuesto
from inventario.models.herramienta import Herramienta
from inventario.models.movimiento import MovimientoInventario

@admin.register(EquipoMedico)
class EquipoMedicoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'marca', 'modelo', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'marca')
    search_fields = ('codigo', 'nombre', 'serie', 'marca', 'modelo')

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'stock', 'stock_minimo', 'precio', 'ubicacion')
    list_filter = ('ubicacion',)
    search_fields = ('codigo', 'nombre', 'ubicacion')

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'marca', 'estado', 'ubicacion')
    list_filter = ('estado', 'marca')
    search_fields = ('codigo', 'nombre', 'marca', 'ubicacion')

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('n_orden', 'fecha', 'tipo', 'repuesto', 'cantidad', 'tecnico')
    list_filter = ('tipo', 'fecha')
    search_fields = ('n_orden', 'repuesto__nombre', 'tecnico__username', 'observaciones')
    readonly_fields = ('n_orden', 'fecha')
