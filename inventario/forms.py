from django import forms
from django.contrib.auth.models import User
from .models import EquipoMedico, MovimientoInventario, Repuesto, Herramienta

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']
        labels = {
            'username': 'Nombre de Usuario',
            'is_staff': 'Es Administrador / Supervisor',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        return username


class EquipoMedicoForm(forms.ModelForm):
    class Meta:
        model = EquipoMedico
        fields = ['codigo', 'nombre', 'marca', 'modelo', 'serie', 'estado', 'descripcion']

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if not codigo.isalnum():
            raise forms.ValidationError("El código del equipo solo debe contener caracteres alfanuméricos.")
        return codigo
    
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        
        fields = ['repuesto', 'tipo', 'cantidad', 'equipo_destino', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'w-full border rounded p-2', 'rows': 3}),
            'repuesto': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'tipo': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'w-full border rounded p-2'}),
            'equipo_destino': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
        }

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['codigo', 'nombre', 'stock', 'stock_minimo', 'precio', 'ubicacion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full border rounded p-2'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'w-full border rounded p-2'}),
            'precio': forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'step': '0.01'}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
        }
class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['codigo', 'nombre', 'marca', 'estado', 'ubicacion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'marca': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'estado': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
        }