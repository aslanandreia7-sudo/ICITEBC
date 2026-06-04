from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
import logging

from .models import Contacto, Inscripcion, Curso, Clase, ProgresoClase

logger = logging.getLogger('django.security')


def home(request):
    enviado = False
    error   = None

    if request.method == 'POST':
        nombre   = request.POST.get('nombre', '').strip()
        email    = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        mensaje  = request.POST.get('mensaje', '').strip()

        if not nombre or not email or not mensaje:
            error = 'Los campos nombre, correo y mensaje son obligatorios.'
        elif len(nombre) > 100:
            error = 'El nombre es demasiado largo.'
        elif len(mensaje) > 2000:
            error = 'El mensaje es demasiado largo.'
        elif len(telefono) > 20:
            error = 'El teléfono no es válido.'
        else:
            try:
                validate_email(email)
                Contacto.objects.create(
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    mensaje=mensaje
                )
                enviado = True
            except ValidationError:
                error = 'El correo electrónico no es válido.'

        if error:
            logger.warning(f'Intento de contacto inválido desde IP: {request.META.get("REMOTE_ADDR")}')

    cursos = Curso.objects.filter(activo=True).order_by('orden')

    return render(request, 'plataforma/index.html', {
        'enviado': enviado,
        'cursos':  cursos,
        'error':   error,
    })


def curso_publico(request, slug):
    curso   = get_object_or_404(Curso, slug=slug, activo=True)
    modulos = curso.modulos.prefetch_related('secciones__clases').all()

    total_minutos = sum(
        clase.duracion_minutos
        for modulo  in modulos
        for seccion in modulo.secciones.all()
        for clase   in seccion.clases.all()
    )
    total_horas = total_minutos // 60
    resto_min   = total_minutos % 60

    return render(request, 'plataforma/curso_publico.html', {
        'curso':         curso,
        'modulos':       modulos,
        'total_minutos': total_minutos,
        'total_horas':   total_horas,
        'resto_min':     resto_min,
        'whatsapp_url':  curso.get_whatsapp_url(),
    })


@login_required
def dashboard(request):
    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user
    ).select_related('curso')

    mis_cursos = inscripciones.filter(estado='aprobado')
    pendientes = inscripciones.filter(estado='pendiente')

    cursos_con_progreso = []
    for insc in mis_cursos:
        cursos_con_progreso.append({
            'inscripcion': insc,
            'curso':       insc.curso,
            'progreso':    insc.progreso(),
        })

    return render(request, 'plataforma/dashboard.html', {
        'cursos_con_progreso': cursos_con_progreso,
        'pendientes':          pendientes,
    })


@login_required
def detalle_curso(request, slug):
    curso       = get_object_or_404(Curso, slug=slug, activo=True)
    inscripcion = get_object_or_404(
        Inscripcion,
        estudiante=request.user,
        curso=curso,
        estado='aprobado'
    )

    completadas_ids = ProgresoClase.objects.filter(
        inscripcion=inscripcion, completada=True
    ).values_list('clase_id', flat=True)

    modulos = curso.modulos.prefetch_related('secciones__clases').all()

    return render(request, 'plataforma/curso_detalle.html', {
        'curso':           curso,
        'modulos':         modulos,
        'completadas_ids': list(completadas_ids),
        'progreso':        inscripcion.progreso(),
    })


@login_required
@require_POST
def marcar_clase(request, clase_id):
    clase       = get_object_or_404(Clase, id=clase_id)
    inscripcion = get_object_or_404(
        Inscripcion,
        estudiante=request.user,
        curso=clase.seccion.modulo.curso,
        estado='aprobado'
    )

    progreso_obj, created = ProgresoClase.objects.get_or_create(
        inscripcion=inscripcion, clase=clase
    )
    progreso_obj.completada       = not progreso_obj.completada
    progreso_obj.fecha_completada = timezone.now() if progreso_obj.completada else None
    progreso_obj.save()

    return JsonResponse({
        'completada':     progreso_obj.completada,
        'progreso_total': inscripcion.progreso(),
    })