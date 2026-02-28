from django.contrib import admin
from django.urls import path, include # Importante agregar 'include'
from plataforma.views import home

urlpatterns = [
    path('admin/', admin.site.urls), # Tu panel técnico
    path('', home, name='home'),      # Tu página principal profesional
    
    # Esta línea activa /accounts/login/ y usa tu plantilla personalizada
    path('accounts/', include('django.contrib.auth.urls')), 
]