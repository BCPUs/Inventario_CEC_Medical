from django.db import models
from django.contrib.auth.models import User

class EquipoMedico(models.Model):
    ESTADO_CHOICES = [
        ('bueno', 'Bueno'),
        ('mantenimiento', 'En Mantenimiento'),
        ('reparacion', 'En Reparación'),
        ('de baja', 'De Baja'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Inventario")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Equipo")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    serie = models.CharField(max_length=100, unique=True, verbose_name="Número de Serie")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='bueno', verbose_name="Estado Operativo")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción/Observaciones")

    def __str__(self):
        return f"{self.nombre} - {self.marca} ({self.codigo})"

    class Meta:
        verbose_name = "Equipo Médico"
        verbose_name_plural = "Equipos Médicos"


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


class Herramienta(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible en Bodega'),
        ('en_uso', 'En Uso / Asignada'),
        ('mantenimiento', 'En Mantenimiento'),
        ('extraviada', 'Extraviada / Dada de Baja'),
    ]
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Herramienta")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Herramienta")
    marca = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marca")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado Actual")
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación Física")

    def __str__(self):
        return f"{self.nombre} - {self.codigo} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Herramienta"
        verbose_name_plural = "Herramientas"


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada (Compra/Devolución)'),
        ('salida', 'Salida (Uso en Mantenimiento)'),
    ]
    
    repuesto = models.ForeignKey('Repuesto', on_delete=models.CASCADE, related_name='movimientos', verbose_name="Repuesto a mover")
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Técnico Responsable")
    equipo_destino = models.ForeignKey('EquipoMedico', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Equipo en Mantenimiento (Solo si es Salida)")
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones / Motivo")

    def save(self, *args, **kwargs):
        if self.pk is None: 
            if self.tipo == 'entrada':
                self.repuesto.stock += self.cantidad
            elif self.tipo == 'salida':
                if self.repuesto.stock < self.cantidad:
                    raise ValueError(f"Stock insuficiente. Solo hay {self.repuesto.stock} unidades de {self.repuesto.nombre}.")
                self.repuesto.stock -= self.cantidad
            
            self.repuesto.save()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.fecha.strftime('%d/%m/%Y')}] {self.get_tipo_display()} - {self.repuesto.nombre} ({self.cantidad} ud)"

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha']