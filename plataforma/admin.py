from django.contrib import admin
from .models import Alumno, Contacto, Curso, Modulo, Seccion, Clase, Inscripcion, ProgresoClase


# --- INLINES ---

class ClaseInline(admin.StackedInline):
    model = Clase
    extra = 1
    fields = ('titulo', 'tipo', 'orden', 'es_gratis',
              'video_url', 'video_archivo', 'pdf_archivo', 'texto', 'duracion_minutos')


class SeccionInline(admin.StackedInline):
    model = Seccion
    extra = 1
    show_change_link = True  # botón para abrir la sección y ver sus clases


class ModuloInline(admin.StackedInline):
    model = Modulo
    extra = 1
    show_change_link = True


# --- ADMIN DE CLASE (edición directa con sus campos) ---

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'seccion', 'tipo', 'orden', 'es_gratis', 'duracion_minutos')
    list_filter   = ('tipo', 'es_gratis', 'seccion__modulo__curso')
    search_fields = ('titulo',)
    ordering      = ('seccion__modulo__orden', 'seccion__orden', 'orden')


# --- ADMIN DE SECCIÓN con sus clases inline ---

@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'orden')
    list_filter  = ('modulo__curso',)
    inlines      = [ClaseInline]


# --- ADMIN DE MÓDULO con sus secciones inline ---

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'orden', 'total_clases')
    list_filter  = ('curso',)
    inlines      = [SeccionInline]


# --- ADMIN DE CURSO — el principal, con módulos inline ---

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'activo', 'precio', 'orden', 'total_clases')
    list_editable = ('activo', 'precio', 'orden')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ModuloInline]


# --- INSCRIPCIONES ---

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'curso', 'estado', 'fecha_inscripcion', 'progreso')
    list_filter   = ('estado', 'curso')
    list_editable = ('estado',)

    def progreso(self, obj):
        return f"{obj.progreso()}%"
    progreso.short_description = "Progreso"


# --- OTROS ---

admin.site.register(Alumno)
admin.site.register(Contacto)
admin.site.register(ProgresoClase)