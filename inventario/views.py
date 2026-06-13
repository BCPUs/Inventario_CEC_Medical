from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import EquipoMedico, MovimientoInventario, Repuesto, Herramienta
from .forms import UserForm, EquipoMedicoForm, MovimientoForm, RepuestoForm, HerramientaForm
from django.contrib import messages


# CONFIGURACIÓN Y ENRUTAMIENTO BASE

def admin_required(user):
    return user.is_staff

def home(request):
    if request.user.is_authenticated:
        return redirect('equipo_list')
    return redirect('login')

# GESTIÓN DE USUARIOS

@login_required
@user_passes_test(admin_required)
def user_list(request):
    usuarios = User.objects.all()
    return render(request, 'inventario/user_list.html', {'usuarios': usuarios})

@login_required
@user_passes_test(admin_required)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'inventario/user_form.html', {'form': form, 'title': 'Registrar Usuario'})


#EQUIPOS MÉDICOS

@login_required
def equipo_list(request):
    equipos = EquipoMedico.objects.all()
    return render(request, 'inventario/equipo_list.html', {'equipos': equipos})

@login_required
def equipo_create(request):
    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipo_list')
    else:
        form = EquipoMedicoForm()
    return render(request, 'inventario/equipo_form.html', {'form': form, 'title': 'Registrar Equipo Médico'})

@login_required
def equipo_update(request):
    pk = request.GET.get('id') or request.POST.get('id')
    equipo = get_object_or_404(EquipoMedico, pk=pk)
    if request.method == 'POST':
        form = EquipoMedicoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('equipo_list')
    else:
        form = EquipoMedicoForm(instance=equipo)
    return render(request, 'inventario/equipo_form.html', {'form': form, 'title': 'Modificar Equipo Médico'})

@login_required
def equipo_delete(request):
    pk = request.GET.get('id') or request.POST.get('id')
    equipo = get_object_or_404(EquipoMedico, pk=pk)
    if request.method == 'POST':
        equipo.delete()
        return redirect('equipo_list')
    return render(request, 'inventario/equipo_confirm_delete.html', {'equipo': equipo})


#REPUESTOS

@login_required
def repuesto_list(request):
    repuestos = Repuesto.objects.all().order_by('nombre')
    return render(request, 'inventario/repuesto_list.html', {'repuestos': repuestos})

@login_required
def repuesto_create(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Repuesto registrado exitosamente.")
            return redirect('repuesto_list')
    else:
        form = RepuestoForm()
    return render(request, 'inventario/repuesto_form.html', {'form': form, 'title': 'Registrar Repuesto'})

@login_required
def repuesto_update(request):
    pk = request.GET.get('id') or request.POST.get('id')
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            form.save()
            messages.success(request, "Repuesto actualizado exitosamente.")
            return redirect('repuesto_list')
    else:
        form = RepuestoForm(instance=repuesto)
    return render(request, 'inventario/repuesto_form.html', {'form': form, 'title': 'Modificar Repuesto'})

@login_required
def repuesto_delete(request):
    pk = request.GET.get('id') or request.POST.get('id')
    repuesto = get_object_or_404(Repuesto, pk=pk)
    
    if repuesto.movimientoinventario_set.exists():
        messages.error(request, f"No se puede eliminar el repuesto '{repuesto.nombre}' porque contiene transacciones activas en el historial de movimientos.")
        return redirect('repuesto_list')
        
    if request.method == 'POST':
        repuesto.delete()
        messages.success(request, "Repuesto eliminado correctamente de los catálogos.")
        return redirect('repuesto_list')
    return render(request, 'inventario/repuesto_confirm_delete.html', {'repuesto': repuesto})

#HERRAMIENTAS

@login_required
def herramienta_list(request):
    herramientas = Herramienta.objects.all().order_by('nombre')
    return render(request, 'inventario/herramienta_list.html', {'herramientas': herramientas})

@login_required
def herramienta_create(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Herramienta registrada exitosamente.")
            return redirect('herramienta_list')
    else:
        form = HerramientaForm()
    return render(request, 'inventario/herramienta_form.html', {'form': form, 'title': 'Registrar Herramienta'})

@login_required
def herramienta_update(request):
    pk = request.GET.get('id') or request.POST.get('id')
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos de la herramienta actualizados.")
            return redirect('herramienta_list')
    else:
        form = HerramientaForm(instance=herramienta)
    return render(request, 'inventario/herramienta_form.html', {'form': form, 'title': 'Modificar Herramienta'})

@login_required
def herramienta_delete(request):
    pk = request.GET.get('id') or request.POST.get('id')
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        herramienta.delete()
        messages.success(request, "Herramienta velocidad eliminada correctamente.")
        return redirect('herramienta_list')
    return render(request, 'inventario/herramienta_confirm_delete.html', {'herramienta': herramienta})


# HISTORIAL DE MOVIMIENTOS (KARDEX)

@login_required
def movimiento_list(request):
    movimientos = MovimientoInventario.objects.all().order_by('-fecha')
    return render(request, 'inventario/movimiento_list.html', {'movimientos': movimientos})

@login_required
def registrar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.tecnico = request.user
            
            try:
                movimiento.save() 
                messages.success(request, "Movimiento registrado. Stock actualizado automáticamente.")
                return redirect('equipo_list') 
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = MovimientoForm()
        
    return render(request, 'inventario/movimiento_form.html', {'form': form})