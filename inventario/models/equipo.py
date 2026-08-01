from django.db import models

class EquipoMedico(models.Model):
    ESTADO_CHOICES = [
        ('bueno', 'Bueno'),
        ('mantenimiento', 'En Mantenimiento'),
        ('reparacion', 'En Reparación'),
        ('de baja', 'De Baja'),
    ]

    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Inventario")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Equipo")
    marca = models.CharField(max_length=100, verbose_name="Marca")  # Increased to max 100 characters per instruction
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
