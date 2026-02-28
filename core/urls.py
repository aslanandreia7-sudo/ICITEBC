from django.contrib import admin
from django.urls import path, include
from plataforma import views  # Importa las vistas de tu app principal
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 1. Panel de Administración (Corregido)
    path('admin/', admin.site.urls),

    # 2. Página de Inicio (Pública)
    path('', views.home, name='home'),

    # 3. Dashboard del Alumno (Privado)
    path('dashboard/', views.dashboard, name='dashboard'),

    # 4. Sistema de Autenticación (Login/Logout)
    # El Login usa el template que tienes en templates/registration/login.html
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # El Logout redirige al Home después de salir
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]