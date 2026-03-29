from django.db import models
from django.contrib.auth.models import User

# --- MODELOS DE USUARIO Y CONTACTO ---

class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


# --- CATÁLOGO DE CURSOS ---

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    # ✅ NUEVOS — para la tarjeta del catálogo público en index.html
    categoria = models.CharField(max_length=100, blank=True, help_text="Ej: Electrónica, IoT, CAD")
    descripcion_corta = models.CharField(max_length=200, blank=True, help_text="Texto corto para la tarjeta del catálogo")

    class Meta:
        ordering = ['orden', 'titulo']

    def __str__(self):
        return self.titulo

    def total_clases(self):
        return Clase.objects.filter(seccion__modulo__curso=self).count()


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.curso.titulo} › {self.titulo}"

    def total_clases(self):
        return Clase.objects.filter(seccion__modulo=self).count()


class Seccion(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='secciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.modulo.titulo} › {self.titulo}"


class Clase(models.Model):
    TIPO_CHOICES = (
        ('video_url',     '🎬 Video (URL / YouTube)'),
        ('video_archivo', '📹 Video (Archivo subido)'),
        ('pdf',           '📄 Archivo PDF'),
        ('texto',         '📝 Texto / Descripción'),
    )
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='clases')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    orden = models.PositiveIntegerField(default=0)
    es_gratis = models.BooleanField(default=False, help_text="Visible sin inscripción")

    # Contenido según tipo
    video_url     = models.URLField(blank=True, null=True, help_text="URL de YouTube o cualquier video")
    video_archivo = models.FileField(upload_to='clases/videos/', blank=True, null=True)
    pdf_archivo   = models.FileField(upload_to='clases/pdfs/', blank=True, null=True)
    texto         = models.TextField(blank=True, null=True, help_text="Contenido en texto o HTML")

    duracion_minutos = models.PositiveIntegerField(default=0, help_text="Duración en minutos (opcional)")

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.seccion.titulo} › {self.titulo}"


# --- INSCRIPCIONES Y PROGRESO ---

class Inscripcion(models.Model):
    ESTADOS = (
        ('pendiente', 'Esperando Aprobación'),
        ('aprobado',  'Activo'),
    )
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('estudiante', 'curso')

    def __str__(self):
        return f"{self.estudiante.username} en {self.curso.titulo}"

    def progreso(self):
        total = self.curso.total_clases()
        if total == 0:
            return 0
        completadas = ProgresoClase.objects.filter(
            inscripcion=self, completada=True
        ).count()
        return int((completadas / total) * 100)


class ProgresoClase(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='progresos')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)
    fecha_completada = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('inscripcion', 'clase')

    def __str__(self):
        return f"{self.inscripcion.estudiante.username} - {self.clase.titulo} ({'✓' if self.completada else '○'})"