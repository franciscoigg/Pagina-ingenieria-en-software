from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)  
    REQUIRED_FIELDS = ['username'] 
    USERNAME_FIELD = 'email' 

    def __str__(self):
        return self.email

class Profesional(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    nombre = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    biografia = models.TextField()
    disponibilidad = models.TextField()
    correo = models.EmailField()  
    telefono = models.CharField(max_length=9)  
    descripcion = models.TextField() 
    foto = models.ImageField(upload_to='profesionales/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    paciente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=15,
        choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
        default='pendiente'
    )

    def __str__(self):
        return f"Cita con {self.profesional.nombre} para {self.paciente.username} el {self.fecha} a las {self.hora}"

class Reseña(models.Model):
    cita = models.OneToOneField(Cita,related_name='reseñas', on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    comentario = models.TextField()