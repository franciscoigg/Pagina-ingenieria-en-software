# app/test/test_forms.py
from django.test import TestCase
from app.forms import ProfesionalForm
from app.models import Profesional, Usuario
from unittest.mock import patch

class TestProfesionalForm(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="testuser@ejemplo.com",
            username="testuser",
            password="contrasena"
        )

    def test_formulario_valido(self):
        data = {
            'nombre': 'Dr. Smith',
            'especialidad': 'Cardiología',
            'ubicacion': 'Ciudad X',
            'biografia': 'Biografía del profesional',
            'disponibilidad': 'Lunes a Viernes',
            'correo': 'dr.smith@ejemplo.com',  
            'telefono': '123456789',  
            'descripcion': 'Descripción del profesional', 
            'foto': None 
        }

        form = ProfesionalForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        profesional = form.save(commit=False)
        profesional.user = self.usuario
        profesional.save()

        self.assertEqual(Profesional.objects.count(), 1)
        self.assertEqual(profesional.nombre, 'Dr. Smith')

