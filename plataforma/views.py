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
            
    # Cambié 'plataforma/index.html' por 'index.html' si es tu página principal
    return render(request, 'index.html', {'enviado': enviado})

@login_required
def dashboard(request):
    # Traemos las inscripciones filtradas por el alumno logueado
    inscripciones = Inscripcion.objects.filter(estudiante=request.user)
    
    mis_cursos = inscripciones.filter(estado='aprobado')
    pendientes = inscripciones.filter(estado='pendiente')
    
    # CORRECCIÓN DE RUTA: Debe coincidir con tu carpeta 'plataforma' y el nombre 'dashboard.html'
    return render(request, 'plataforma/dashboard.html', {
        'mis_cursos': mis_cursos,
        'pendientes': pendientes
    })