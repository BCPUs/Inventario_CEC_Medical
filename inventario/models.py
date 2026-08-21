from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Marca(models.Model):
    CATEGORIA_CHOICES = [
        ('medico', 'Equipo Médico'),
        ('herramienta', 'Herramienta'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Marca")
    categoria = models.CharField(
        max_length=20, 
        choices=CATEGORIA_CHOICES, 
        default='medico', 
        verbose_name="Categoría de Uso"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nombre']


class EquipoMedico(models.Model):
    ESTADO_CHOICES = [
        ('bueno', 'Bueno / Operativo'),
        ('mantenimiento', 'En Mantenimiento Preventivo'),
        ('reparacion', 'En Reparación Crítica'),
        ('de baja', 'De Baja Definitiva'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Inventario")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Equipo")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='equipos', verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    serie = models.CharField(max_length=100, unique=True, verbose_name="Número de Serie")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='bueno', verbose_name="Estado Operativo")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción/Observaciones")

    def __str__(self):
        return f"{self.nombre} - {self.marca.nombre} ({self.codigo})"

    class Meta:
        verbose_name = "Equipo Médico"
        verbose_name_plural = "Equipos Médicos"


class Repuesto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Repuesto")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Repuesto")
    
    # Restricción a nivel de campo (no permite valores < 0)
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Stock")
    stock_minimo = models.PositiveIntegerField(default=2, verbose_name="Stock Mínimo Alerta")
    
    # Validador para Formularios y Admin (no admite precios en negativo)
    precio = models.DecimalField(
        decimal_places=2, 
        max_digits=10, 
        validators=[MinValueValidator(0.00)],
        verbose_name="Precio Unitario"
    )
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación en Bodega")

    def __str__(self):
        return f"{self.nombre} (Disponibles: {self.stock})"

    class Meta:
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"

        constraints = [
            models.CheckConstraint(
                check=models.Q(stock__gte=0),
                name='repuesto_stock_no_negativo'
            ),
            models.CheckConstraint(
                check=models.Q(precio__gte=0),
                name='repuesto_precio_no_negativo'
            )
        ]


class Herramienta(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible en Bodega'),
        ('en_uso', 'En Uso / Asignada'),
        ('mantenimiento', 'En Mantenimiento'),
        ('extraviada', 'Extraviada / Dada de Baja'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Herramienta")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Herramienta")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='herramientas', verbose_name="Marca", null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado Actual")
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación Física")

    def __str__(self):
        return f"{self.nombre} - {self.codigo} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Herramienta"
        verbose_name_plural = "Herramientas"


class OrdenTrabajo(models.Model):
    ESTADO_ORDEN = [
        ('abierta', 'Recibido / En Diagnóstico'),
        ('reparada', 'Reparado / Listo'),
        ('sin_reparacion', 'No Reparar / De Baja'),
    ]
    
    secuencial = models.CharField(max_length=20, unique=True, verbose_name="N° Orden de Trabajo", editable=False)
    equipo = models.ForeignKey(EquipoMedico, on_delete=models.CASCADE, related_name='ordenes', verbose_name="Equipo Recibido")
    tecnico = models.CharField(max_length=150, verbose_name="Técnico Responsable")
    diagnostico_falla = models.TextField(verbose_name="Falla Reportada / Diagnóstico")
    estado = models.CharField(max_length=20, choices=ESTADO_ORDEN, default='abierta', verbose_name="Estado de Reparación")
    fecha_ingreso = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Recepción")
    fecha_finalizacion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Cierre")

    def save(self, *args, **kwargs):
        if not self.secuencial:
            ultima_orden = OrdenTrabajo.objects.all().order_by('id').last()
            siguiente_num = (ultima_orden.id + 1) if ultima_orden else 1
            self.secuencial = f"{siguiente_num:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OT-{self.secuencial} ({self.equipo.nombre})"

    class Meta:
        verbose_name = "Orden de Trabajo"
        verbose_name_plural = "Órdenes de Trabajo"
        ordering = ['-fecha_ingreso']


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('compra', 'Compra (Ingreso a Bodega)'),
        ('egreso', 'Egreso (Uso en Orden de Trabajo)'),
        ('devolucion', 'Devolución (Retorno desde Reparación)'),
    ]
    
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='movimientos', verbose_name="Repuesto")
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Registrado Por")
    orden_trabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, null=True, blank=True, related_name='insumos', verbose_name="Orden de Trabajo Vinculada")
    
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora Transacción")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones / Justificación")

    def clean(self):
        """Validación preventiva antes de guardar (formularios/admin)"""
        super().clean()
        if self.tipo == 'egreso' and self.repuesto_id and self.cantidad:
            if self.repuesto.stock < self.cantidad:
                raise ValidationError({
                    'cantidad': f"Stock insuficiente en bodega. Solo dispones de {self.repuesto.stock} unidad(es) de {self.repuesto.nombre}."
                })

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk is None: 
            if self.tipo in ['compra', 'devolucion']:
                self.repuesto.stock += self.cantidad
            elif self.tipo == 'egreso':
                if self.repuesto.stock < self.cantidad:
                    raise ValueError(f"Stock insuficiente en Bodega. Solo dispone de {self.repuesto.stock} unidades de {self.repuesto.nombre}.")
                self.repuesto.stock -= self.cantidad
            
            self.repuesto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.repuesto.nombre} x {self.cantidad}"

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha']