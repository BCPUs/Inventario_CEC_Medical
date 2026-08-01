from django import forms
from inventario.models.herramienta import Herramienta

class HerramientaForm(forms.ModelForm):
    codigo = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
        label="Código de Herramienta",
        error_messages={
            'max_length': "Código de herramienta: máximo 50 caracteres."
        }
    )
    marca = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
        label="Marca",
        error_messages={
            'max_length': "Marca: máximo 100 caracteres."
        }
    )

    class Meta:
        model = Herramienta
        fields = ['codigo', 'nombre', 'marca', 'estado', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'estado': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
        }
