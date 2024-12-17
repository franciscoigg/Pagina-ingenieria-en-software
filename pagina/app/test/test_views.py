# app/test/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import Profesional, Cita, Reseña
from django.test import Client

# Usamos el User modelo que está configurado en settings.AUTH_USER_MODEL
User = get_user_model()

@pytest.mark.django_db
def test_index_view(client):
    user = User.objects.create_user(email='testuser@example.com', password='password', username='testuser')
    
    client.login(email='testuser@example.com', password='password')
 
    response = client.get(reverse('inicio'))
    
    assert 'Bienvenido' in response.content.decode()

@pytest.mark.django_db
def test_reserva_view(client):

    user = User.objects.create_user(email='testuser@example.com', password='password', username='testuser')
    
    client.login(email='testuser@example.com', password='password')
    
    profesional = Profesional.objects.create(
        user=user,
        nombre="Dr. Juan",
        especialidad="Psicología",
        ubicacion="Ciudad X",
        biografia="Psicólogo especializado en...",
        disponibilidad="Lunes a Viernes 9am - 6pm",
        correo="drjuan@example.com",
        telefono="1234567890",
        descripcion="Descripción del profesional",
    )
    
    response = client.get(reverse('reserva'))
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_agregar_resena_view(client):

    user = get_user_model().objects.create_user(
        email='testuser@example.com',
        password='password',
        username='testuser'
    )

    client.login(email='testuser@example.com', password='password')

    profesional = Profesional.objects.create(
        user=user,
        nombre="Dr. Juan",
        especialidad="Psicología",
        ubicacion="Ciudad X",
        biografia="Psicólogo especializado en...",
        disponibilidad="Lunes a Viernes 9am - 6pm",
        correo="drjuan@example.com",
        telefono="1234567890",
        descripcion="Descripción del profesional",
    )

    cita = Cita.objects.create(
        paciente=user,
        profesional=profesional,
        fecha='2024-12-16',
        hora='10:00:00',
        estado='pendiente',
    )

    response = client.get(reverse('resena', args=[cita.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_agregar_profesional_view():

    User = get_user_model()
    user = User.objects.create_user(email="testuser@example.com", password="password",username='testuser')


    profesional = Profesional.objects.create(
        user=user,
        nombre="Dr. Juan",
        especialidad="Psicología",
        ubicacion="Ciudad X",
        biografia="Psicólogo especializado en...",
        disponibilidad="Lunes a Viernes 9am - 6pm",
        correo="drjuan@example.com",
        telefono="1234567890",
        descripcion="Descripción del profesional"
    )

    client = Client()
    client.login(email="testuser@example.com", password="password")

    response = client.get(reverse('agregar_profesional'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_cancelar_cita_view(client):

    user = get_user_model().objects.create_user(
        email='testuser@example.com',
        password='password',
        username='testuser'
    )

    client.login(email='testuser@example.com', password='password')

    profesional = Profesional.objects.create(
        user=user,
        nombre="Dr. Juan",
        especialidad="Psicología",
        ubicacion="Ciudad X",
        biografia="Psicólogo especializado en...",
        disponibilidad="Lunes a Viernes 9am - 6pm",
        correo="drjuan@example.com",
        telefono="1234567890",
        descripcion="Descripción del profesional",
    )

    cita = Cita.objects.create(
        paciente=user,
        profesional=profesional,
        fecha='2024-12-16',
        hora='10:00:00',
        estado='pendiente',
    )

    response = client.get(reverse('cancelar_cita', args=[cita.id]))

    assert response.status_code == 302

@pytest.mark.django_db
def test_profesionales_view(client):

    user = User.objects.create_user(email='testuser@example.com', password='password', username='testuser')
    
    client.login(email='testuser@example.com', password='password')

    profesional = Profesional.objects.create(
        user=user,
        nombre="Dr. Juan",
        especialidad="Psicología",
        ubicacion="Ciudad X",
        biografia="Psicólogo especializado en...",
        disponibilidad="Lunes a Viernes 9am - 6pm",
        correo="drjuan@example.com",
        telefono="1234567890",
        descripcion="Descripción del profesional",
    )
    
    response = client.get(reverse('profesionales'))
    
    assert response.status_code == 200
    assert 'Dr. Juan' in response.content.decode()

@pytest.mark.django_db
def test_ver_profesional_view(client):

    user = User.objects.create_user(email='testuser@example.com', password='password', username='testuser')
    
    client.login(email='testuser@example.com', password='password')
    
    profesional = Profesional.objects.create(
        user=user,
        nombre="Dr. Juan",
        especialidad="Psicología",
        ubicacion="Ciudad X",
        biografia="Psicólogo especializado en...",
        disponibilidad="Lunes a Viernes 9am - 6pm",
        correo="drjuan@example.com",
        telefono="1234567890",
        descripcion="Descripción del profesional",
    )
    
    response = client.get(reverse('ver_profesional', kwargs={'profesional_id': profesional.id}))

    assert response.status_code == 200
    assert 'Dr. Juan' in response.content.decode()
