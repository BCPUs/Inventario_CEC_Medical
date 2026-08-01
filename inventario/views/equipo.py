from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventario.forms.equipo import EquipoMedicoForm
from inventario.services.equipo_service import (
    listar_equipos,
    obtener_equipo_por_id,
    registrar_equipo,
    eliminar_equipo
)

@login_required
def equipo_list(request):
    equipos = listar_equipos()
    return render(request, 'inventario/equipo_list.html', {'equipos': equipos})

@login_required
def equipo_create(request):
    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST)
        if form.is_valid():
            registrar_equipo(form)
            return redirect('equipo_list')
    else:
        form = EquipoMedicoForm()
    return render(request, 'inventario/equipo_form.html', {'form': form, 'title': 'Registrar Equipo Médico'})

@login_required
def equipo_update(request):
    pk = request.GET.get('id') or request.POST.get('id')
    equipo = obtener_equipo_por_id(pk)
    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST, instance=equipo)
        if form.is_valid():
            registrar_equipo(form)
            return redirect('equipo_list')
    else:
        form = EquipoMedicoForm(instance=equipo)
    return render(request, 'inventario/equipo_form.html', {'form': form, 'title': 'Modificar Equipo Médico'})

@login_required
def equipo_delete(request):
    pk = request.GET.get('id') or request.POST.get('id')
    equipo = obtener_equipo_por_id(pk)
    if request.method == 'POST':
        eliminar_equipo(equipo)
        return redirect('equipo_list')
    return render(request, 'inventario/equipo_confirm_delete.html', {'equipo': equipo})
