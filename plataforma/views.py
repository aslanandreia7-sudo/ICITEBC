from django.shortcuts import render
from .models import Contacto

def home(request):
    enviado = False
    if request.method == 'POST':
        # Capturamos los datos del formulario de tu index.html
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        # Creamos el registro en la base de datos
        if nombre and email and mensaje:
            Contacto.objects.create(
                nombre=nombre, 
                email=email, 
                mensaje=mensaje
            )
            enviado = True # Esto activa el mensaje de éxito en el HTML
            
    return render(request, 'plataforma/index.html', {'enviado': enviado})