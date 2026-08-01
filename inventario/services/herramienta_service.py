from inventario.models.herramienta import Herramienta

def listar_herramientas():
    return Herramienta.objects.all().order_by('nombre')

def obtener_herramienta_por_id(herramienta_id):
    from django.shortcuts import get_object_or_404
    return get_object_or_404(Herramienta, pk=herramienta_id)

def registrar_herramienta(form_data_or_instance):
    if hasattr(form_data_or_instance, 'save'):
        return form_data_or_instance.save()
    herramienta = Herramienta(**form_data_or_instance)
    herramienta.save()
    return herramienta

def eliminar_herramienta(herramienta):
    herramienta.delete()
