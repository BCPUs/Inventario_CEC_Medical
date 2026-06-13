from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Autenticación nativa
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # CRUD Usuarios 
    path('usuarios/', views.user_list, name='user_list'),
    path('usuarios/nuevo/', views.user_create, name='user_create'),
    
    # CRUD Equipos 
    path('equipos/', views.equipo_list, name='equipo_list'),
    path('equipos/nuevo/', views.equipo_create, name='equipo_create'),
    path('equipos/editar/', views.equipo_update, name='equipo_update'),
    path('equipos/eliminar/', views.equipo_delete, name='equipo_delete'),

    # Movimientos - Kardex (Solo Inserción y Lectura por Auditoría)
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/nuevo/', views.registrar_movimiento, name='registrar_movimiento'),

    # CRUD Repuestos 
    path('repuestos/', views.repuesto_list, name='repuesto_list'),
    path('repuestos/nuevo/', views.repuesto_create, name='repuesto_create'),
    path('repuestos/editar/', views.repuesto_update, name='repuesto_update'),
    path('repuestos/eliminar/', views.repuesto_delete, name='repuesto_delete'),

    # CRUD Herramientas 
    path('herramientas/', views.herramienta_list, name='herramienta_list'),
    path('herramientas/nuevo/', views.herramienta_create, name='herramienta_create'),
    path('herramientas/editar/', views.herramienta_update, name='herramienta_update'),
    path('herramientas/eliminar/', views.herramienta_delete, name='herramienta_delete'),
]