from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages

from .models import (
    EquipoMedico,
    MovimientoInventario,
    Repuesto,
    Herramienta,
    Marca,
    OrdenTrabajo
)

from .forms import (
    UserForm,
    EquipoMedicoForm,
    RepuestoForm,
    HerramientaForm,
    MarcaForm,
    OrdenTrabajoForm,
    MovimientoOrdenForm
)


def admin_required(user):
    return user.is_staff


def home(request):

    if request.user.is_authenticated:
        return redirect('orden_list')

    return redirect('login')


# ============================================================
# MARCAS
# ============================================================

@login_required
def marca_list(request):

    marcas = Marca.objects.all().order_by(
        'categoria',
        'nombre'
    )

    return render(
        request,
        'inventario/marca_list.html',
        {'marcas': marcas}
    )


@login_required
def marca_create(request):

    if request.method == 'POST':

        form = MarcaForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Nueva marca estandarizada agregada correctamente."
            )

            return redirect('marca_list')

    else:

        form = MarcaForm()

    return render(
        request,
        'inventario/marca_form.html',
        {
            'form': form,
            'title': 'Crear Marca Estándar'
        }
    )


@login_required
def marca_update(request):

    pk = request.GET.get('id') or request.POST.get('id')

    marca = get_object_or_404(
        Marca,
        pk=pk
    )

    if request.method == 'POST':

        form = MarcaForm(
            request.POST,
            instance=marca
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Catálogo de marca modificado con éxito."
            )

            return redirect('marca_list')

    else:

        form = MarcaForm(
            instance=marca
        )

    return render(
        request,
        'inventario/marca_form.html',
        {
            'form': form,
            'title': 'Modificar Marca'
        }
    )


# ============================================================
# ÓRDENES DE TRABAJO
# ============================================================

@login_required
def orden_list(request):

    ordenes = OrdenTrabajo.objects.all()

    return render(
        request,
        'inventario/orden_list.html',
        {
            'ordenes': ordenes
        }
    )


@login_required
def orden_create(request):

    if request.method == 'POST':

        form = OrdenTrabajoForm(request.POST)

        if form.is_valid():

            orden = form.save()

            # Al recibir el equipo se marca como
            # "En Reparación"
            orden.equipo.estado = 'reparacion'
            orden.equipo.save()

            messages.success(
                request,
                f"Orden OT-{orden.secuencial} aperturada. "
                f"Equipo configurado como 'En Reparación'."
            )

            return redirect(
                'orden_detail',
                pk=orden.pk
            )

    else:

        form = OrdenTrabajoForm()

    return render(
        request,
        'inventario/orden_form.html',
        {
            'form': form,
            'title': 'Recepción de Equipo - Orden de Trabajo'
        }
    )


@login_required
def orden_detail(request, pk):

    orden = get_object_or_404(
        OrdenTrabajo,
        pk=pk
    )

    insumos_utilizados = orden.insumos.all()

    return render(
        request,
        'inventario/orden_detail.html',
        {
            'orden': orden,
            'insumos': insumos_utilizados
        }
    )


# ============================================================
# INICIAR REPARACIÓN
# ============================================================

@login_required
def orden_iniciar(request, pk):

    orden = get_object_or_404(
        OrdenTrabajo,
        pk=pk
    )

    if request.method != 'POST':

        return redirect(
            'orden_detail',
            pk=orden.pk
        )

    # Solo se puede iniciar desde diagnóstico
    if orden.estado != 'abierta':

        messages.error(
            request,
            "Esta orden ya no se encuentra en estado de diagnóstico."
        )

        return redirect(
            'orden_detail',
            pk=orden.pk
        )

    # Cambiar a EN PROCESO
    orden.estado = 'en_proceso'
    orden.save()

    messages.success(
        request,
        f"La Orden de Trabajo OT-{orden.secuencial} "
        f"pasó a estado 'En Proceso'."
    )

    return redirect(
        'orden_detail',
        pk=orden.pk
    )


# ============================================================
# AGREGAR REPUESTO
# ============================================================

@login_required
def orden_agregar_repuesto(request, pk):

    orden = get_object_or_404(
        OrdenTrabajo,
        pk=pk
    )

    # Se pueden agregar repuestos mientras la orden
    # esté abierta o en proceso.
    if orden.estado not in ['abierta', 'en_proceso']:

        messages.error(
            request,
            "No puede alterar una orden finalizada."
        )

        return redirect(
            'orden_detail',
            pk=orden.pk
        )

    if request.method == 'POST':

        form = MovimientoOrdenForm(
            request.POST
        )

        if form.is_valid():

            movimiento = form.save(
                commit=False
            )

            movimiento.orden_trabajo = orden
            movimiento.tecnico = request.user
            movimiento.tipo = 'egreso'

            try:

                movimiento.save()

                messages.success(
                    request,
                    f"Insumo "
                    f"{movimiento.repuesto.nombre} "
                    f"agregado correctamente a la orden."
                )

                return redirect(
                    'orden_detail',
                    pk=orden.pk
                )

            except ValueError as e:

                messages.error(
                    request,
                    str(e)
                )

    else:

        form = MovimientoOrdenForm()

    return render(
        request,
        'inventario/orden_add_repuesto.html',
        {
            'form': form,
            'orden': orden
        }
    )


# ============================================================
# DEVOLVER REPUESTO
# ============================================================

@login_required
def orden_devolver_repuesto(request, mov_id):

    movimiento_origen = get_object_or_404(
        MovimientoInventario,
        pk=mov_id,
        tipo='egreso'
    )

    orden = movimiento_origen.orden_trabajo

    # La devolución solamente se permite mediante POST
    if request.method != 'POST':
        return redirect('orden_detail', pk=orden.pk)

    # No permitir devoluciones cuando la OT ya terminó
    if orden.estado not in ['abierta', 'en_proceso']:
        messages.error(
            request,
            "No puede devolver repuestos de una orden finalizada."
        )
        return redirect('orden_detail', pk=orden.pk)

    # Evitar devolver dos veces el mismo movimiento
    if (
        movimiento_origen.observaciones
        and '[REVERTIDO / DEVUELTO]' in movimiento_origen.observaciones
    ):
        messages.error(
            request,
            "Este repuesto ya fue devuelto al inventario."
        )
        return redirect('orden_detail', pk=orden.pk)

    # Crear movimiento de devolución
    MovimientoInventario.objects.create(
        repuesto=movimiento_origen.repuesto,
        tecnico=request.user,
        orden_trabajo=orden,
        tipo='devolucion',
        cantidad=movimiento_origen.cantidad,
        observaciones=(
            f"Devolución del movimiento #{movimiento_origen.id}"
        )
    )

    # Marcar el movimiento original como devuelto
    movimiento_origen.observaciones = (
        f"[REVERTIDO / DEVUELTO] "
        f"{movimiento_origen.observaciones or ''}"
    )

    movimiento_origen.save()

    messages.success(
        request,
        f"Se devolvieron {movimiento_origen.cantidad} unidades de "
        f"{movimiento_origen.repuesto.nombre} al inventario."
    )

    return redirect(
        'orden_detail',
        pk=orden.pk
    )

# ============================================================
# CERRAR ORDEN
# ============================================================

@login_required
def orden_cerrar(request, pk):

    orden = get_object_or_404(
        OrdenTrabajo,
        pk=pk
    )

    if request.method != 'POST':

        return redirect(
            'orden_detail',
            pk=orden.pk
        )

    # Solo se puede cerrar una orden abierta o en proceso
    if orden.estado not in ['abierta', 'en_proceso']:

        messages.error(
            request,
            "Esta Orden de Trabajo ya se encuentra finalizada."
        )

        return redirect(
            'orden_detail',
            pk=orden.pk
        )

    estado_cierre = request.POST.get(
        'estado_cierre'
    )

    if estado_cierre not in [
        'reparada',
        'sin_reparacion'
    ]:

        messages.error(
            request,
            "Estado de finalización no válido."
        )

        return redirect(
            'orden_detail',
            pk=orden.pk
        )

    # Guardar estado de la orden
    orden.estado = estado_cierre

    # Guardar fecha de finalización
    orden.fecha_finalizacion = timezone.now()

    orden.save()

    # Actualizar estado del equipo
    if estado_cierre == 'reparada':

        orden.equipo.estado = 'bueno'

    else:

        orden.equipo.estado = 'de baja'

    orden.equipo.save()

    # Mensaje final
    if estado_cierre == 'reparada':

        messages.success(
            request,
            f"OT-{orden.secuencial} finalizada correctamente. "
            f"El equipo fue marcado como operativo."
        )

    else:

        messages.warning(
            request,
            f"OT-{orden.secuencial} finalizada. "
            f"El equipo fue marcado como de baja."
        )

    return redirect(
        'orden_detail',
        pk=orden.pk
    )


# ============================================================
# USUARIOS
# ============================================================

@login_required
@user_passes_test(admin_required)
def user_list(request):

    usuarios = User.objects.all()

    return render(
        request,
        'inventario/user_list.html',
        {
            'usuarios': usuarios
        }
    )


@login_required
@user_passes_test(admin_required)
def user_create(request):

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            user = form.save(
                commit=False
            )

            if form.cleaned_data['password']:

                user.set_password(
                    form.cleaned_data['password']
                )

            user.save()

            return redirect(
                'user_list'
            )

    else:

        form = UserForm()

    return render(
        request,
        'inventario/user_form.html',
        {
            'form': form,
            'title': 'Registrar Usuario'
        }
    )


# ============================================================
# EQUIPOS MÉDICOS
# ============================================================

@login_required
def equipo_list(request):

    equipos = EquipoMedico.objects.all()

    return render(
        request,
        'inventario/equipo_list.html',
        {
            'equipos': equipos
        }
    )


@login_required
def equipo_create(request):

    if request.method == 'POST':

        form = EquipoMedicoForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'equipo_list'
            )

    else:

        form = EquipoMedicoForm()

    return render(
        request,
        'inventario/equipo_form.html',
        {
            'form': form,
            'title': 'Registrar Equipo Médico'
        }
    )


@login_required
def equipo_update(request):

    pk = (
        request.GET.get('id')
        or request.POST.get('id')
    )

    equipo = get_object_or_404(
        EquipoMedico,
        pk=pk
    )

    if request.method == 'POST':

        form = EquipoMedicoForm(
            request.POST,
            instance=equipo
        )

        if form.is_valid():

            form.save()

            return redirect(
                'equipo_list'
            )

    else:

        form = EquipoMedicoForm(
            instance=equipo
        )

    return render(
        request,
        'inventario/equipo_form.html',
        {
            'form': form,
            'title': 'Modificar Equipo Médico'
        }
    )


@login_required
def equipo_delete(request):

    pk = (
        request.GET.get('id')
        or request.POST.get('id')
    )

    equipo = get_object_or_404(
        EquipoMedico,
        pk=pk
    )

    if request.method == 'POST':

        equipo.delete()

        return redirect(
            'equipo_list'
        )

    return render(
        request,
        'inventario/equipo_confirm_delete.html',
        {
            'equipo': equipo
        }
    )


# ============================================================
# REPUESTOS
# ============================================================

@login_required
def repuesto_list(request):

    repuestos = Repuesto.objects.all().order_by(
        'nombre'
    )

    return render(
        request,
        'inventario/repuesto_list.html',
        {
            'repuestos': repuestos
        }
    )


@login_required
def repuesto_create(request):

    if request.method == 'POST':

        form = RepuestoForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Repuesto registrado exitosamente."
            )

            return redirect(
                'repuesto_list'
            )

    else:

        form = RepuestoForm()

    return render(
        request,
        'inventario/repuesto_form.html',
        {
            'form': form,
            'title': 'Registrar Repuesto'
        }
    )


@login_required
def repuesto_update(request):

    pk = (
        request.GET.get('id')
        or request.POST.get('id')
    )

    repuesto = get_object_or_404(
        Repuesto,
        pk=pk
    )

    if request.method == 'POST':

        form = RepuestoForm(
            request.POST,
            instance=repuesto
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Repuesto actualizado exitosamente."
            )

            return redirect(
                'repuesto_list'
            )

    else:

        form = RepuestoForm(
            instance=repuesto
        )

    return render(
        request,
        'inventario/repuesto_form.html',
        {
            'form': form,
            'title': 'Modificar Repuesto'
        }
    )


@login_required
def repuesto_delete(request):

    pk = (
        request.GET.get('id')
        or request.POST.get('id')
    )

    repuesto = get_object_or_404(
        Repuesto,
        pk=pk
    )

    if repuesto.movimientos.exists():

        messages.error(
            request,
            f"Imposible eliminar "
            f"'{repuesto.nombre}' debido a "
            f"transacciones indexadas en el Kardex."
        )

        return redirect(
            'repuesto_list'
        )

    if request.method == 'POST':

        repuesto.delete()

        messages.success(
            request,
            "Repuesto removido de catálogos."
        )

        return redirect(
            'repuesto_list'
        )

    return render(
        request,
        'inventario/repuesto_confirm_delete.html',
        {
            'repuesto': repuesto
        }
    )


# ============================================================
# HERRAMIENTAS
# ============================================================

@login_required
def herramienta_list(request):

    herramientas = Herramienta.objects.all().order_by(
        'nombre'
    )

    return render(
        request,
        'inventario/herramienta_list.html',
        {
            'herramientas': herramientas
        }
    )


@login_required
def herramienta_create(request):

    if request.method == 'POST':

        form = HerramientaForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Herramienta registrada."
            )

            return redirect(
                'herramienta_list'
            )

    else:

        form = HerramientaForm()

    return render(
        request,
        'inventario/herramienta_form.html',
        {
            'form': form,
            'title': 'Registrar Herramienta'
        }
    )


@login_required
def herramienta_update(request):

    pk = (
        request.GET.get('id')
        or request.POST.get('id')
    )

    herramienta = get_object_or_404(
        Herramienta,
        pk=pk
    )

    if request.method == 'POST':

        form = HerramientaForm(
            request.POST,
            instance=herramienta
        )

        if form.is_valid():

            form.save()

            return redirect(
                'herramienta_list'
            )

    else:

        form = HerramientaForm(
            instance=herramienta
        )

    return render(
        request,
        'inventario/herramienta_form.html',
        {
            'form': form,
            'title': 'Modificar Herramienta'
        }
    )


@login_required
def herramienta_delete(request):

    pk = (
        request.GET.get('id')
        or request.POST.get('id')
    )

    herramienta = get_object_or_404(
        Herramienta,
        pk=pk
    )

    if request.method == 'POST':

        herramienta.delete()

        return redirect(
            'herramienta_list'
        )

    return render(
        request,
        'inventario/herramienta_confirm_delete.html',
        {
            'herramienta': herramienta
        }
    )


# ============================================================
# MOVIMIENTOS / KARDEX
# ============================================================

@login_required
def movimiento_list(request):

    movimientos = MovimientoInventario.objects.all().order_by(
        '-fecha'
    )

    return render(
        request,
        'inventario/movimiento_list.html',
        {
            'movimientos': movimientos
        }
    )

# ============================================================
# REGISTRAR INGRESO DE REPUESTO
# ============================================================

@login_required
def movimiento_ingreso(request):

    if request.method == 'POST':

        repuesto_id = request.POST.get('repuesto')
        cantidad = request.POST.get('cantidad')
        observaciones = request.POST.get('observaciones')

        repuesto = get_object_or_404(
            Repuesto,
            pk=repuesto_id
        )

        try:
            cantidad = int(cantidad)

            if cantidad <= 0:
                raise ValueError

        except (ValueError, TypeError):

            messages.error(
                request,
                "La cantidad debe ser un número mayor que cero."
            )

            return redirect('movimiento_ingreso')

        MovimientoInventario.objects.create(
            repuesto=repuesto,
            tecnico=request.user,
            tipo='compra',
            cantidad=cantidad,
            observaciones=observaciones or "Ingreso de repuesto a bodega."
        )

        messages.success(
            request,
            f"Ingreso registrado correctamente. "
            f"Se agregaron {cantidad} unidades de "
            f"{repuesto.nombre} al inventario."
        )

        return redirect('movimiento_list')

    repuestos = Repuesto.objects.all().order_by('nombre')

    return render(
        request,
        'inventario/movimiento_ingreso.html',
        {
            'repuestos': repuestos
        }
    )