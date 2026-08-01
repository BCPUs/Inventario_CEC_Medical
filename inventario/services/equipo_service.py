from inventario.models.equipo import EquipoMedico

def listar_equipos():
    return EquipoMedico.objects.all()

def obtener_equipo_por_id(equipo_id):
    from django.shortcuts import get_object_or_404
    return get_object_or_404(EquipoMedico, pk=equipo_id)

def registrar_equipo(form_data_or_instance):
    if hasattr(form_data_or_instance, 'save'):
        return form_data_or_instance.save()
    equipo = EquipoMedico(**form_data_or_instance)
    equipo.save()
    return equipo

def eliminar_equipo(equipo):
    equipo.delete()
