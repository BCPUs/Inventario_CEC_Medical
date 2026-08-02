from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .repuesto import Repuesto
from .equipo import EquipoMedico

class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada (Compra/Devolución)'),
        ('salida', 'Salida (Uso en Mantenimiento)'),
    ]

    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='movimientos', verbose_name="Repuesto a mover")
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Técnico Responsable")
    equipo_destino = models.ForeignKey(EquipoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Equipo en Mantenimiento (Solo si es Salida)")

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(0, message="El valor no puede ser negativo.")],
        verbose_name="Cantidad"
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones / Motivo")

    # Auto-generated sequential order number (n_orden), unique and not editable
    n_orden = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Número de Orden")

    def __str__(self):
        return f"[{self.fecha.strftime('%d/%m/%Y') if self.fecha else 'Nueva'}] {self.get_tipo_display()} - {self.repuesto.nombre} ({self.cantidad} ud) - Order: {self.n_orden}"

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha']
