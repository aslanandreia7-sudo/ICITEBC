from django.contrib import admin
from .models import Alumno, Contacto, Curso, Modulo, Seccion, Clase, Inscripcion, ProgresoClase

# --- PERSONALIZACIÓN DEL SITIO ADMIN ---
admin.site.site_header  = "ICITEBC — Panel de Gestión"
admin.site.site_title   = "ICITEBC Admin"
admin.site.index_title  = "Bienvenido al panel de administración"


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
    list_per_page = 50


# --- ADMIN DE SECCIÓN ---

@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'modulo', 'orden')
    list_filter   = ('modulo__curso',)
    inlines       = [ClaseInline]
    list_per_page = 50


# --- ADMIN DE MÓDULO ---

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'curso', 'orden', 'total_clases')
    list_filter   = ('curso',)
    inlines       = [SeccionInline]
    list_per_page = 50


# --- ADMIN DE CURSO ---

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display        = ('titulo', 'activo', 'precio_general', 'fecha_proxima', 'orden', 'total_clases')
    list_editable       = ('activo', 'orden')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines             = [ModuloInline]
    list_per_page       = 25

    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'slug', 'categoria', 'activo', 'orden', 'imagen')
        }),
        ('Descripción', {
            'fields': ('descripcion_corta', 'descripcion', 'descripcion_larga'),
        }),
        ('Logística del Curso', {
            'fields': ('duracion', 'modalidad', 'nivel', 'dirigido_a', 'cupo_maximo', 'fecha_proxima'),
        }),
        ('Precios', {
            'fields': ('precio', 'precio_general', 'precio_descuento', 'precio_descuento_label', 'anticipo'),
        }),
        ('WhatsApp y Contacto', {
    'fields': ('whatsapp_numero', 'whatsapp_mensaje', 'stripe_payment_link'),
}),
    )


# --- INSCRIPCIONES ---

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display   = ('estudiante', 'curso', 'estado', 'fecha_inscripcion', 'mostrar_progreso')
    list_filter    = ('estado', 'curso')
    list_editable  = ('estado',)
    list_per_page  = 50
    # Campos que no se deben modificar manualmente
    readonly_fields = ('estudiante', 'curso', 'fecha_inscripcion')

    def mostrar_progreso(self, obj):
        return f"{obj.progreso()}%"
    mostrar_progreso.short_description = "Progreso"


# --- CONTACTO (solo lectura para proteger datos) ---

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display   = ('nombre', 'email', 'fecha', 'leido')
    list_filter    = ('leido',)
    list_editable  = ('leido',)
    list_per_page  = 50
    readonly_fields = ('nombre', 'email', 'mensaje', 'fecha')  # Nadie puede editar mensajes
    search_fields  = ('nombre', 'email')

    def has_add_permission(self, request):
        return False  # Nadie puede crear contactos desde el admin


# --- ALUMNO ---

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display  = ('user', 'departamento', 'correo_institucional', 'fecha_registro')
    search_fields = ('user__username', 'correo_institucional')
    readonly_fields = ('fecha_registro',)
    list_per_page = 50


# --- PROGRESO (solo lectura) ---

@admin.register(ProgresoClase)
class ProgresoClaseAdmin(admin.ModelAdmin):
    list_display    = ('inscripcion', 'clase', 'completada', 'fecha_completada')
    list_filter     = ('completada',)
    readonly_fields = ('inscripcion', 'clase', 'completada', 'fecha_completada')
    list_per_page   = 50

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False