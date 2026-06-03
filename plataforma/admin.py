from django.contrib import admin
from .models import Alumno, Contacto, Curso, Modulo, Seccion, Clase, Inscripcion, ProgresoClase


# --- INLINES ---

class ClaseInline(admin.StackedInline):
    model  = Clase
    extra  = 1
    fields = (
        'titulo', 'tipo', 'orden', 'es_gratis',
        'video_url', 'video_archivo', 'pdf_archivo', 'texto', 'duracion_minutos'
    )


class SeccionInline(admin.StackedInline):
    model            = Seccion
    extra            = 1
    show_change_link = True


class ModuloInline(admin.StackedInline):
    model            = Modulo
    extra            = 1
    show_change_link = True


# --- ADMIN DE CLASE ---

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'seccion', 'tipo', 'orden', 'es_gratis', 'duracion_minutos')
    list_filter   = ('tipo', 'es_gratis', 'seccion__modulo__curso')
    search_fields = ('titulo',)
    ordering      = ('seccion__modulo__orden', 'seccion__orden', 'orden')


# --- ADMIN DE SECCIÓN ---

@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'orden')
    list_filter  = ('modulo__curso',)
    inlines      = [ClaseInline]


# --- ADMIN DE MÓDULO ---

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'orden', 'total_clases')
    list_filter  = ('curso',)
    inlines      = [SeccionInline]


# --- ADMIN DE CURSO ---

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display        = ('titulo', 'activo', 'precio_general', 'fecha_proxima', 'orden', 'total_clases')
    list_editable       = ('activo', 'orden')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines             = [ModuloInline]

    fieldsets = (
        ('📋 Información Básica', {
            'fields': ('titulo', 'slug', 'categoria', 'activo', 'orden', 'imagen')
        }),
        ('📝 Descripción', {
            'fields': ('descripcion_corta', 'descripcion', 'descripcion_larga'),
            'description': 'descripcion_corta aparece en la tarjeta del catálogo. '
                           'descripcion_larga aparece en la página completa del curso.'
        }),
        ('📅 Logística del Curso', {
            'fields': ('duracion', 'modalidad', 'nivel', 'dirigido_a', 'cupo_maximo', 'fecha_proxima'),
        }),
        ('💰 Precios', {
            'fields': ('precio', 'precio_general', 'precio_descuento', 'precio_descuento_label', 'anticipo'),
            'description': 'precio = campo original para la plataforma interna. '
                           'precio_general y precio_descuento se muestran en la página pública del curso.'
        }),
        ('📱 WhatsApp & Contacto', {
            'fields': ('whatsapp_numero', 'whatsapp_mensaje'),
            'description': 'El mensaje puede quedar vacío — se genera automáticamente con el nombre del curso.'
        }),
    )


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