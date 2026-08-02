from django import forms
from inventario.models.equipo import EquipoMedico

class EquipoMedicoForm(forms.ModelForm):
    marca = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
        label="Marca",
        error_messages={
            'max_length': "Marca: máximo 100 caracteres."
        }
    )

    class Meta:
        model = EquipoMedico
        fields = ['codigo', 'nombre', 'marca', 'modelo', 'serie', 'estado', 'descripcion']

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if not codigo.isalnum():
            raise forms.ValidationError("El código del equipo solo debe contener caracteres alfanuméricos.")
        return codigo
