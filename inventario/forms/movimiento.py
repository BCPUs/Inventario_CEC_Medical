from django import forms
from inventario.models.movimiento import MovimientoInventario

class MovimientoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'min': '0'}),
        label="Cantidad",
        error_messages={
            'min_value': "El valor no puede ser negativo.",
        }
    )

    class Meta:
        model = MovimientoInventario
        fields = ['repuesto', 'tipo', 'cantidad', 'equipo_destino', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'w-full border rounded p-2', 'rows': 3}),
            'repuesto': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'tipo': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'equipo_destino': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise forms.ValidationError("El valor no puede ser negativo.")
        return cantidad

    def clean(self):
        cleaned_data = super().clean()
        repuesto = cleaned_data.get('repuesto')
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')

        if repuesto and tipo == 'salida' and cantidad is not None:
            if repuesto.stock < cantidad:
                raise forms.ValidationError(
                    f"No existe suficiente stock disponible. Stock disponible: {repuesto.stock}"
                )
        return cleaned_data
