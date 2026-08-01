from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from inventario.forms.usuario import UserForm
from inventario.services.usuario_service import listar_usuarios, registrar_usuario

def admin_required(user):
    return user.is_staff

@login_required
@user_passes_test(admin_required)
def user_list(request):
    usuarios = listar_usuarios()
    return render(request, 'inventario/user_list.html', {'usuarios': usuarios})

@login_required
@user_passes_test(admin_required)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            registrar_usuario(form)
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'inventario/user_form.html', {'form': form, 'title': 'Registrar Usuario'})
