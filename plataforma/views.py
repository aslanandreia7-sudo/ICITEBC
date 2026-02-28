from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Contacto, Inscripcion, Curso

def home(request):
    enviado = False
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        if nombre and email and mensaje:
            Contacto.objects.create(
                nombre=nombre, 
                email=email, 
                mensaje=mensaje
            )
            enviado = True 
            
    # Asumiendo que index.html está en plataforma/templates/plataforma/
    return render(request, 'plataforma/index.html', {'enviado': enviado})

@login_required
def dashboard(request):
    # Optimizamos la consulta trayendo solo lo del usuario actual
    inscripciones = Inscripcion.objects.filter(estudiante=request.user)
    
    mis_cursos = inscripciones.filter(estado='aprobado')
    pendientes = inscripciones.filter(estado='pendiente')
    
    # RUTA CORREGIDA según tu estructura de carpetas en VS Code
    return render(request, 'plataforma/dashboard.html', {
        'mis_cursos': mis_cursos,
        'pendientes': pendientes
    })