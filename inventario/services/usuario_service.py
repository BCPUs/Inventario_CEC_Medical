from django.contrib.auth.models import User

def listar_usuarios():
    return User.objects.all()

def registrar_usuario(form_instance):
    user = form_instance.save(commit=False)
    if form_instance.cleaned_data.get('password'):
        user.set_password(form_instance.cleaned_data['password'])
    user.save()
    return user
