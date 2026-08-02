from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from inventario.models.equipo import EquipoMedico
from inventario.models.repuesto import Repuesto
from inventario.models.herramienta import Herramienta
from inventario.models.movimiento import MovimientoInventario
from inventario.forms.repuesto import RepuestoForm
from inventario.forms.herramienta import HerramientaForm
from inventario.forms.movimiento import MovimientoForm
from inventario.services.movimiento_service import registrar_movimiento_servicio

class InventarioValidationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_tecnico", password="password")
        self.repuesto = Repuesto.objects.create(
            codigo="REP-001",
            nombre="Batería de Respaldo",
            stock=10,
            stock_minimo=2,
            precio=15.50,
            ubicacion="Estantería A"
        )
        self.equipo = EquipoMedico.objects.create(
            codigo="EQ01",
            nombre="Desfibrilador",
            marca="Phillips",
            modelo="HeartStart",
            serie="SN12345"
        )

    def test_stock_not_negative_validation_in_form(self):
        # Repuesto form: test stock cannot be negative
        data = {
            'codigo': 'REP-002',
            'nombre': 'Filtro de Aire',
            'stock': -5,
            'stock_minimo': 2,
            'precio': '12.50',
            'ubicacion': 'Estantería B'
        }
        form = RepuestoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)
        self.assertEqual(form.errors['stock'][0], "El valor no puede ser negativo.")

    def test_precio_not_negative_validation_in_form(self):
        # Repuesto form: test price cannot be negative
        data = {
            'codigo': 'REP-002',
            'nombre': 'Filtro de Aire',
            'stock': 5,
            'stock_minimo': 2,
            'precio': '-12.50',
            'ubicacion': 'Estantería B'
        }
        form = RepuestoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)
        self.assertEqual(form.errors['precio'][0], "El precio no puede ser negativo.")

    def test_decimal_separator_dot_only(self):
        # Repuesto form: test only dot allowed as decimal separator
        # Note: forms fetch raw data from .data, we simulate this with a QueryDict or dict data passed
        data = {
            'codigo': 'REP-002',
            'nombre': 'Filtro de Aire',
            'stock': 5,
            'stock_minimo': 2,
            'precio': '12,50',  # comma used
            'ubicacion': 'Estantería B'
        }
        form = RepuestoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)
        self.assertEqual(form.errors['precio'][0], "Utilice punto (.) como separador decimal.")

    def test_herramienta_code_and_brand_limits(self):
        # Herramienta code max 50 characters, brand max 100 characters
        long_code = "H" * 51
        long_brand = "B" * 101

        data = {
            'codigo': long_code,
            'nombre': 'Martillo',
            'marca': 'Standard',
            'estado': 'disponible',
            'ubicacion': 'Bodega Central'
        }
        form = HerramientaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('codigo', form.errors)
        self.assertEqual(form.errors['codigo'][0], "Código de herramienta: máximo 50 caracteres.")

        data = {
            'codigo': 'HERR-01',
            'nombre': 'Martillo',
            'marca': long_brand,
            'estado': 'disponible',
            'ubicacion': 'Bodega Central'
        }
        form = HerramientaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('marca', form.errors)
        self.assertEqual(form.errors['marca'][0], "Marca: máximo 100 caracteres.")

    def test_movimiento_negative_quantity(self):
        # Movimiento form: quantity cannot be negative
        data = {
            'repuesto': self.repuesto.id,
            'tipo': 'entrada',
            'cantidad': -10,
            'equipo_destino': '',
            'observaciones': 'Prueba'
        }
        form = MovimientoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad', form.errors)
        self.assertEqual(form.errors['cantidad'][0], "El valor no puede ser negativo.")

    def test_movimiento_withdraw_exceeds_available_stock(self):
        # Movimiento form: cannot withdraw more stock than available
        # Current stock is 10
        data = {
            'repuesto': self.repuesto.id,
            'tipo': 'salida',
            'cantidad': 15,
            'equipo_destino': self.equipo.id,
            'observaciones': 'Prueba de salida excesiva'
        }
        form = MovimientoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'][0], "No existe suficiente stock disponible. Stock disponible: 10")

    def test_auto_generation_of_sequential_order_number(self):
        # Movimiento register service should auto-generate sequential ORD-XXXX
        # Movement 1
        data = {
            'repuesto': self.repuesto.id,
            'tipo': 'entrada',
            'cantidad': 5,
            'equipo_destino': '',
            'observaciones': 'Primera entrada'
        }
        form1 = MovimientoForm(data=data)
        self.assertTrue(form1.is_valid())
        mov1 = registrar_movimiento_servicio(form1, self.user)
        self.assertEqual(mov1.n_orden, "ORD-0001")

        # Check that stock increased: 10 + 5 = 15
        self.repuesto.refresh_from_db()
        self.assertEqual(self.repuesto.stock, 15)

        # Movement 2
        data2 = {
            'repuesto': self.repuesto.id,
            'tipo': 'salida',
            'cantidad': 3,
            'equipo_destino': self.equipo.id,
            'observaciones': 'Segunda salida'
        }
        form2 = MovimientoForm(data=data2)
        self.assertTrue(form2.is_valid())
        mov2 = registrar_movimiento_servicio(form2, self.user)
        self.assertEqual(mov2.n_orden, "ORD-0002")

        # Check that stock decreased: 15 - 3 = 12
        self.repuesto.refresh_from_db()
        self.assertEqual(self.repuesto.stock, 12)
