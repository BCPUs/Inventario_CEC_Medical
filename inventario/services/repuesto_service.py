from inventario.models.repuesto import Repuesto

def listar_repuestos():
    return Repuesto.objects.all().order_by('nombre')

def obtener_repuesto_por_id(repuesto_id):
    from django.shortcuts import get_object_or_404
    return get_object_or_404(Repuesto, pk=repuesto_id)

def registrar_repuesto(form_data_or_instance):
    if hasattr(form_data_or_instance, 'save'):
        return form_data_or_instance.save()
    repuesto = Repuesto(**form_data_or_instance)
    repuesto.save()
    return repuesto

def puede_eliminar_repuesto(repuesto):
    return not repuesto.movimientos.exists()

def eliminar_repuesto(repuesto):
    repuesto.delete()
