from django import forms
from django.contrib.auth.models import User

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
