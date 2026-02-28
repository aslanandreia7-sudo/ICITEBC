from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    # Conectamos con el usuario base de Django (para el login)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Tus campos personalizados
    departamento = models.CharField(max_length=100)
    correo_institucional = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.departamento}"

# --- ESTA ES LA PARTE NUEVA QUE DEBES PEGAR ABAJO ---

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.email}"