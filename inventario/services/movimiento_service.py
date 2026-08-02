from django.db import transaction
from django.core.exceptions import ValidationError
from inventario.models.movimiento import MovimientoInventario

def listar_movimientos():
    return MovimientoInventario.objects.all().order_by('-fecha')

def generar_siguiente_orden():
    # Helper to generate ORD-XXXX auto sequence number
    last_mov = MovimientoInventario.objects.exclude(n_orden='').order_by('-id').first()
    if not last_mov:
        return "ORD-0001"

    # Try to parse the last n_orden
    try:
        if last_mov.n_orden.startswith("ORD-"):
            num_part = int(last_mov.n_orden.replace("ORD-", ""))
            return f"ORD-{num_part + 1:04d}"
    except (ValueError, TypeError):
        pass

    # Fallback to id-based generation
    next_id = MovimientoInventario.objects.count() + 1
    return f"ORD-{next_id:04d}"

def registrar_movimiento_servicio(form_instance, tecnico_user):
    # This service encapsulates all movement business logic, stock adjustments, and auto-ordering
    # Running inside an atomic transaction to ensure data integrity
    with transaction.atomic():
        movimiento = form_instance.save(commit=False)
        movimiento.tecnico = tecnico_user

        # Validate that stock, price, quantities are non-negative
        repuesto = movimiento.repuesto

        if movimiento.cantidad < 0:
            raise ValidationError("El valor no puede ser negativo.")

        if movimiento.tipo == 'entrada':
            repuesto.stock += movimiento.cantidad
        elif movimiento.tipo == 'salida':
            if repuesto.stock < movimiento.cantidad:
                raise ValidationError(f"No existe suficiente stock disponible. Stock disponible: {repuesto.stock}")
            repuesto.stock -= movimiento.cantidad

        # Ensure repuesto doesn't end up negative
        if repuesto.stock < 0:
            raise ValidationError("El valor no puede ser negativo.")

        # Check if the record already has an order number, so we don't overwrite it when editing
        if not movimiento.n_orden:
            movimiento.n_orden = generar_siguiente_orden()

        # Save updated objects
        repuesto.save()
        movimiento.save()
        return movimiento
