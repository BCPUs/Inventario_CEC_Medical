from django.db import models

class Herramienta(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible en Bodega'),
        ('en_uso', 'En Uso / Asignada'),
        ('mantenimiento', 'En Mantenimiento'),
        ('extraviada', 'Extraviada / Dada de Baja'),
    ]
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Herramienta") # Max 50 characters
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Herramienta")
    marca = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca") # Brand: max 100 characters per instruction
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado Actual")
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación Física")

    def __str__(self):
        return f"{self.nombre} - {self.codigo} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Herramienta"
        verbose_name_plural = "Herramientas"
