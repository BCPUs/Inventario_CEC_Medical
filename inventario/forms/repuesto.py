from django import forms
from django.core.validators import MinValueValidator
from inventario.models.repuesto import Repuesto

class RepuestoForm(forms.ModelForm):
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'step': '0.01', 'min': '0'}),
        label="Precio Unitario",
        error_messages={
            'invalid': "Utilice punto (.) como separador decimal.",
        }
    )

    class Meta:
        model = Repuesto
        fields = ['codigo', 'nombre', 'stock', 'stock_minimo', 'precio', 'ubicacion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'min': '0'}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
        }

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El valor no puede ser negativo.")
        return stock

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo is not None and stock_minimo < 0:
            raise forms.ValidationError("El valor no puede ser negativo.")
        return stock_minimo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")

        # Validation for decimal separator: Only dot (.) is allowed.
        raw_precio = self.data.get('precio')
        if raw_precio and ',' in str(raw_precio):
            raise forms.ValidationError("Utilice punto (.) como separador decimal.")

        return precio
