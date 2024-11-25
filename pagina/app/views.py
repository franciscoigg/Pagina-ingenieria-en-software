from django.shortcuts import render, redirect, get_object_or_404
from app.models import Profesional,Cita
from app.forms import ReservaForm, ReseñaForm, ProfesionalForm, RegistroForm, ContactoForm,Reseña
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import EmailLoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def contactanos(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email'] 
        
            messages.success(request, f'Gracias por contactarnos, {nombre}. Te responderemos pronto en {email}.')
            
            return render(request, 'app/contacto.html', {'form': form})
        else:
            messages.error(request, 'Hubo un error con tu envío. Por favor, revisa los campos.')
    else:
        form = ContactoForm()

    return render(request, 'app/contacto.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # Autenticar al usuario después del registro
            return redirect('inicio')  # Redirigir a la página principal
    else:
        form = RegistroForm()
    return render(request, 'app/registro.html', {'form': form})

class Login(LoginView):
    template_name = 'app/login.html'
    authentication_form = EmailLoginForm

def index(request):
    return render(request, 'app/index.html')

def profesionales(request):
    profesionales = Profesional.objects.all()  # Obtener todos los profesionales sin filtro
    return render(request, 'app/profesionales.html', {'profesionales': profesionales})

def ver_profesional(request, profesional_id):
    # Obtener el profesional
    profesional = get_object_or_404(Profesional, id=profesional_id)

    # Obtener todas las citas del profesional
    citas = Cita.objects.filter(profesional=profesional)

    # Obtener todas las reseñas asociadas a las citas de ese profesional
    reseñas = Reseña.objects.filter(cita__in=citas)

    return render(request, 'app/ver_profesional.html', {
        'profesional': profesional,
        'reseñas': reseñas,
    })

@login_required
def reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user  # Asocia el paciente autenticado
            cita.save()
            messages.success(request, "Cita reservada exitosamente.")
            return redirect('inicio')  # Redirige al inicio después de guardar
    else:
        form = ReservaForm()

    return render(request, 'app/reservar.html', {'form': form})

def agregar_resena(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    # Verificar si ya existe una reseña para esta cita
    if Reseña.objects.filter(cita=cita).exists():
        messages.error(request, "Ya has dejado una reseña para esta cita.")
        return redirect('citas')

    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            # Asociamos la reseña con la cita actual
            reseña = form.save(commit=False)
            reseña.cita = cita
            reseña.save()

            messages.success(request, "Tu reseña ha sido agregada correctamente.")
            return redirect('citas')  # Redirigir al usuario a sus citas
    else:
        form = ReseñaForm()

    return render(request, 'app/agregar_resena.html', {'form': form, 'cita': cita})

@login_required
def agregar_profesional(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_profesionales')  # Redirige a una página donde se listan los profesionales
    else:
        form = ProfesionalForm()
    return render(request, 'agregar_profesional.html', {'form': form})


@login_required
def tus_citas(request):
    if request.user.is_staff:  # Si el usuario es un profesional (staff)
        # Filtra las citas basadas en el profesional (usuario) que ha iniciado sesión
        citas = Cita.objects.filter(profesional__user=request.user)  # Solo las citas del profesional
        reseñas = Reseña.objects.filter(cita__profesional__user=request.user)  # Reseñas asociadas a citas de este profesional
        
        return render(request, 'app/citas_profesional.html', {'citas': citas, 'reseñas': reseñas})
    else:
        # Si el usuario no es un profesional, solo muestra sus propias citas
        citas = Cita.objects.filter(paciente=request.user)
        return render(request, 'app/citas.html', {'citas': citas})


@login_required
def cancelar_cita(request, cita_id):
    # Obtener la cita
    try:
        cita = Cita.objects.get(id=cita_id)
    except Cita.DoesNotExist:
        messages.error(request, "La cita que intentas cancelar no existe.")
        return redirect('citas')  # Redirigir a 'tus_citas' si la cita no existe

    # Cambiar el estado de la cita a 'cancelada'
    cita.estado = 'cancelada'
    cita.save()

    # Redirigir al usuario a la vista de 'tus_citas'
    return redirect('citas')

def ver_resenas(request):
    if request.user.is_staff:
        # Obtener el profesional correspondiente
        profesional = Profesional.objects.get(user=request.user)
        
        # Obtener todas las reseñas asociadas a las citas de este profesional
        reseñas = Reseña.objects.filter(cita__profesional=profesional)
        
        return render(request, 'app/ver_resenas.html', {'reseñas': reseñas})
    else:
        # Si no es un profesional, redirige a sus citas
        return redirect('citas')