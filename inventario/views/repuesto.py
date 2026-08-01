from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventario.forms.repuesto import RepuestoForm
from inventario.services.repuesto_service import (
    listar_repuestos,
    obtener_repuesto_por_id,
    registrar_repuesto,
    puede_eliminar_repuesto,
    eliminar_repuesto
)

@login_required
def repuesto_list(request):
    repuestos = listar_repuestos()
    return render(request, 'inventario/repuesto_list.html', {'repuestos': repuestos})

@login_required
def repuesto_create(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            registrar_repuesto(form)
            messages.success(request, "Repuesto registrado exitosamente.")
            return redirect('repuesto_list')
    else:
        form = RepuestoForm()
    return render(request, 'inventario/repuesto_form.html', {'form': form, 'title': 'Registrar Repuesto'})

@login_required
def repuesto_update(request):
    pk = request.GET.get('id') or request.POST.get('id')
    repuesto = obtener_repuesto_por_id(pk)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            registrar_repuesto(form)
            messages.success(request, "Repuesto actualizado exitosamente.")
            return redirect('repuesto_list')
    else:
        form = RepuestoForm(instance=repuesto)
    return render(request, 'inventario/repuesto_form.html', {'form': form, 'title': 'Modificar Repuesto'})

@login_required
def repuesto_delete(request):
    pk = request.GET.get('id') or request.POST.get('id')
    repuesto = obtener_repuesto_por_id(pk)

    if not puede_eliminar_repuesto(repuesto):
        messages.error(request, f"No se puede eliminar el repuesto '{repuesto.nombre}' porque contiene transacciones activas en el historial de movimientos.")
        return redirect('repuesto_list')

    if request.method == 'POST':
        eliminar_repuesto(repuesto)
        messages.success(request, "Repuesto eliminado correctamente de los catálogos.")
        return redirect('repuesto_list')
    return render(request, 'inventario/repuesto_confirm_delete.html', {'repuesto': repuesto})
