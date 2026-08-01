from django.db import models

class Repuesto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Repuesto")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Repuesto")
    stock = models.IntegerField(default=0, verbose_name="Cantidad en Stock")
    stock_minimo = models.IntegerField(default=2, verbose_name="Stock Mínimo Alerta")
    precio = models.DecimalField(max_length=10, decimal_places=2, max_digits=10, verbose_name="Precio Unitario")
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación en Bodega")

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"

    class Meta:
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"
