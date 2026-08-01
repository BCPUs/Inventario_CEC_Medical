from django import forms
from inventario.models.movimiento import MovimientoInventario

class MovimientoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full border rounded p-2'}),
        label="Cantidad",
        error_messages={
            'min_value': "No permitir cantidades negativas.",
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

    def clean(self):
        cleaned_data = super().clean()
        repuesto = cleaned_data.get('repuesto')
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')

        if repuesto and tipo == 'salida' and cantidad is not None:
            if repuesto.stock < cantidad:
                raise forms.ValidationError(
                    "No permitir retirar más stock del disponible."
                )
        return cleaned_data
