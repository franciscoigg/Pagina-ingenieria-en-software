from django.test import TestCase
from app.models import Profesional, Cita, Usuario
from django.utils import timezone
from unittest.mock import patch
from django.db import IntegrityError

class TestProfesionalModel(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="testuser@ejemplo.com", 
            username="testuser", 
            password="contrasena"
        )
        self.profesional = Profesional.objects.create(
            user=self.usuario,
            nombre="Dr. Smith",
            especialidad="Cardiología",
            ubicacion="Ciudad X",
            biografia="Biografía del profesional",
            disponibilidad="Lunes a Viernes",
            correo="dr.smith@ejemplo.com",
            telefono="123456789",
            descripcion="Descripción del profesional"
        )

    def test_profesional_str(self):
        self.assertEqual(str(self.profesional), "Dr. Smith")

    def test_creacion_cita(self):
        cita = Cita.objects.create(
            paciente=self.usuario,
            profesional=self.profesional,
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            estado='pendiente'
        )
        self.assertEqual(cita.estado, 'pendiente')
        self.assertEqual(cita.paciente, self.usuario)
        self.assertEqual(cita.profesional, self.profesional)
