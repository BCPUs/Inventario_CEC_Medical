from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventario.forms.herramienta import HerramientaForm
from inventario.services.herramienta_service import (
    listar_herramientas,
    obtener_herramienta_por_id,
    registrar_herramienta,
    eliminar_herramienta
)

@login_required
def herramienta_list(request):
    herramientas = listar_herramientas()
    return render(request, 'inventario/herramienta_list.html', {'herramientas': herramientas})

@login_required
def herramienta_create(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST)
        if form.is_valid():
            registrar_herramienta(form)
            messages.success(request, "Herramienta registrada exitosamente.")
            return redirect('herramienta_list')
    else:
        form = HerramientaForm()
    return render(request, 'inventario/herramienta_form.html', {'form': form, 'title': 'Registrar Herramienta'})

@login_required
def herramienta_update(request):
    pk = request.GET.get('id') or request.POST.get('id')
    herramienta = obtener_herramienta_por_id(pk)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            registrar_herramienta(form)
            messages.success(request, "Datos de la herramienta actualizados.")
            return redirect('herramienta_list')
    else:
        form = HerramientaForm(instance=herramienta)
    return render(request, 'inventario/herramienta_form.html', {'form': form, 'title': 'Modificar Herramienta'})

@login_required
def herramienta_delete(request):
    pk = request.GET.get('id') or request.POST.get('id')
    herramienta = obtener_herramienta_por_id(pk)
    if request.method == 'POST':
        eliminar_herramienta(herramienta)
        messages.success(request, "Herramienta velocidad eliminada correctamente.")
        return redirect('herramienta_list')
    return render(request, 'inventario/herramienta_confirm_delete.html', {'herramienta': herramienta})
