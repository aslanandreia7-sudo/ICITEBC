from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import Contacto, Inscripcion, Curso, Clase, ProgresoClase


def home(request):
    enviado = False
    if request.method == 'POST':
        nombre  = request.POST.get('nombre')
        email   = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        if nombre and email and mensaje:
            Contacto.objects.create(nombre=nombre, email=email, mensaje=mensaje)
            enviado = True

    cursos = Curso.objects.filter(activo=True).order_by('orden')

    return render(request, 'plataforma/index.html', {
        'enviado': enviado,
        'cursos':  cursos,
    })


def curso_publico(request, slug):
    """
    Página pública del curso — sin login.
    Muestra descripción, temario completo (módulos › secciones › clases)
    y CTA de WhatsApp para apartar lugar.
    """
    curso   = get_object_or_404(Curso, slug=slug, activo=True)
    modulos = curso.modulos.prefetch_related('secciones__clases').all()

    # Total de horas / minutos del curso sumando duracion_minutos de las clases
    total_minutos = sum(
        clase.duracion_minutos
        for modulo  in modulos
        for seccion in modulo.secciones.all()
        for clase   in seccion.clases.all()
    )
    total_horas = total_minutos // 60
    resto_min   = total_minutos % 60

    return render(request, 'plataforma/curso_publico.html', {
        'curso':        curso,
        'modulos':      modulos,
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
    curso        = get_object_or_404(Curso, slug=slug, activo=True)
    inscripcion  = get_object_or_404(Inscripcion, estudiante=request.user, curso=curso, estado='aprobado')

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
def marcar_clase(request, clase_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

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