from django import forms
from django.contrib.auth.models import User
from .models import EquipoMedico, MovimientoInventario, Repuesto, Herramienta, Marca, OrdenTrabajo

class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500'})
            else:
                field.widget.attrs.update({'class': 'w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all'})

class UserForm(TailwindFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']

class MarcaForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'categoria'] 

class EquipoMedicoForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = EquipoMedico
        fields = ['codigo', 'nombre', 'marca', 'modelo', 'serie', 'estado', 'descripcion']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marca'].queryset = Marca.objects.filter(categoria='medico')

class RepuestoForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['codigo', 'nombre', 'stock', 'stock_minimo', 'precio', 'ubicacion']

class HerramientaForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['codigo', 'nombre', 'marca', 'estado', 'ubicacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marca'].queryset = Marca.objects.filter(categoria='herramienta')

class OrdenTrabajoForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['secuencial', 'equipo', 'tecnico', 'diagnostico_falla']
        widgets = {'diagnostico_falla': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describa el estado en el que se recibe el equipo y la avería detectada...'})}

class MovimientoOrdenForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['repuesto', 'cantidad', 'observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej. Sustitución por desgaste estructural.'})}