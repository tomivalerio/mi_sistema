from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clientes.urls')),  # Incluye las URLs de la aplicación "clientes"
]