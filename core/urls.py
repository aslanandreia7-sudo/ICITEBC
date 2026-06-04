from django.contrib import admin
from django.urls import path, include
from plataforma import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Panel de Administración — URL oculta
    path('gestion-ic1t3bc-2025/', admin.site.urls),

    # 2. Página de Inicio (Pública)
    path('', views.home, name='home'),

    # 3. Dashboard del Alumno (Privado)
    path('dashboard/', views.dashboard, name='dashboard'),

    # 4. Página pública del curso
    path('info/<slug:slug>/', views.curso_publico, name='curso_publico'),

    # 5. Detalle del curso para alumnos inscritos
    path('curso/<slug:slug>/', views.detalle_curso, name='detalle_curso'),

    # 6. Marcar clase completada (AJAX)
    path('clase/<int:clase_id>/marcar/', views.marcar_clase, name='marcar_clase'),

    # 7. Login / Logout
    path('accounts/login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)