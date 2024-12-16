from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import Login, registro

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', registro, name='registro'),
    path('', views.index, name='inicio'),
    path('contacto/', views.contactanos, name='contacto'),
    path('agregar-profesional/', views.agregar_profesional, name='agregar_profesional'),
    path('profesionales/', views.profesionales, name='profesionales'),
    path('profesional/<int:profesional_id>/', views.ver_profesional, name='ver_profesional'),
    path('ver_resenas/', views.ver_resenas, name='ver_resenas'),
    path('cancelar_cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('confirmar_cita/<int:cita_id>/', views.confirmar_cita, name='confirmar_cita'),
    path('reserva/', views.reserva, name='reserva'),
    path('citas/', views.tus_citas, name='citas'),
    path('resena/<int:cita_id>', views.agregar_resena, name='resena'),
]