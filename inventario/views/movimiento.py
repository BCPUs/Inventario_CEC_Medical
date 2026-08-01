from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from inventario.forms.movimiento import MovimientoForm
from inventario.services.movimiento_service import listar_movimientos, registrar_movimiento_servicio

@login_required
def movimiento_list(request):
    movimientos = listar_movimientos()
    return render(request, 'inventario/movimiento_list.html', {'movimientos': movimientos})

@login_required
def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            try:
                registrar_movimiento_servicio(form, request.user)
                messages.success(request, "Movimiento registrado. Stock actualizado automáticamente.")
                return redirect('equipo_list')
            except ValidationError as e:
                # Add service-level validation errors to form to show on same screen
                form.add_error(None, e.message if hasattr(e, 'message') else str(e))
    else:
        form = MovimientoForm()

    return render(request, 'inventario/movimiento_form.html', {'form': form})
