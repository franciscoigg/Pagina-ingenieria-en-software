from django import forms
from .models import Cita, Profesional, Reseña
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.models import Usuario



class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'}))
    especialidad = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Especialidad'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Correo Electrónico'}))

class RegistroForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password1', 'password2']

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class ReservaForm(forms.ModelForm):
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),
        label="Selecciona un Profesional",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Fecha de la Cita"
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        label="Hora de la Cita"
    )

    class Meta:
        model = Cita
        fields = ['profesional', 'fecha', 'hora']

    def save(self, commit=True):
        cita = super().save(commit=False)
        if commit:
            cita.save()
        return cita

class ReseñaForm(forms.ModelForm):
    calificacion = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5
        }),
        label="Calificación (1-5)"
    )
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu comentario aquí...'
        }),
        label="Comentario"
    )

    class Meta:
        model = Reseña
        fields = ['calificacion', 'comentario']        

class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['nombre', 'especialidad', 'ubicacion', 'biografia', 'disponibilidad', 'correo', 'telefono', 'descripcion', 'foto']
        widgets = {
            'disponibilidad': forms.Textarea(attrs={'rows': 3}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        # Establecer is_staff a True para hacer al profesional un 'staff'
        profesional = super().save(commit=False)
        if commit:
            # Aquí también puedes establecer el 'is_staff' del User asociado
            user = profesional.user  # Suponiendo que tienes una relación con el User
            user.is_staff = True
            user.save()
            profesional.save()
        return profesional