from django.contrib import admin
from django.urls import path
from plataforma import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('gestion-ic1t3bc-2025/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('info/<slug:slug>/', views.curso_publico, name='curso_publico'),
    path('curso/<slug:slug>/', views.detalle_curso, name='detalle_curso'),
    path('clase/<int:clase_id>/marcar/', views.marcar_clase, name='marcar_clase'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=os.path.join(settings.BASE_DIR, 'media'))