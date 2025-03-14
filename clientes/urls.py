from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Página de login como página principal
    path('login/', views.login_view, name='login'),  # Ruta adicional para login
    path('logout/', views.logout_view, name='logout'),
    path('panel/', views.panel, name='panel'),
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('editar-cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar-cliente/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('movimientos-cliente/<int:id>/', views.movimientos_cliente, name='movimientos_cliente'),
    path('agregar-movimiento/<int:id>/', views.agregar_movimiento, name='agregar_movimiento'),
    path('editar-movimiento/<int:id>/', views.editar_movimiento, name='editar_movimiento'),
    path('eliminar-movimiento/<int:id>/', views.eliminar_movimiento, name='eliminar_movimiento'),
]