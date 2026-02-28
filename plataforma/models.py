from django.db import models
from django.contrib.auth.models import User

# --- MODELOS DE USUARIO Y CONTACTO ---

class Alumno(models.Model):
    # Conectamos con el usuario base de Django (para el login)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Tus campos personalizados
    departamento = models.CharField(max_length=100)
    correo_institucional = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.departamento}"

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.email}"


# --- NUEVOS MODELOS DE CURSOS ---

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='cursos/')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.titulo

class Inscripcion(models.Model):
    ESTADOS = (
        ('pendiente', 'Esperando Aprobación'),
        ('aprobado', 'Activo'),
    )
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    progreso = models.IntegerField(default=0) # Porcentaje 0-100

    class Meta:
        # Evita que un estudiante se inscriba dos veces al mismo curso
        unique_together = ('estudiante', 'curso')

    def __str__(self):
        return f"{self.estudiante.username} en {self.curso.titulo}"