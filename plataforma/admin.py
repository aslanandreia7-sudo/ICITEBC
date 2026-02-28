from django.contrib import admin
from .models import Alumno, Contacto # Agrega Contacto aquí

admin.site.register(Alumno)
admin.site.register(Contacto) # Y esta línea