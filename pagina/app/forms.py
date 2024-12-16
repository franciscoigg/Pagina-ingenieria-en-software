# Importaciones necesarias
from django import forms
from .models import Cita, Profesional, Reseña  # Modelos de la aplicación
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # Formularios de autenticación y registro de usuario
from app.models import Usuario  # Modelo de Usuario personalizado

# Formulario de contacto para la página de contacto
class ContactoForm(forms.Form):
    """
    Formulario utilizado para el contacto, recoge el nombre, especialidad y correo electrónico del usuario.
    """
    # Campo para el nombre del contacto
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'}))
    # Campo para la especialidad del contacto
    especialidad = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Especialidad'}))
    # Campo para el correo electrónico del contacto
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Correo Electrónico'}))

# Formulario para el registro de nuevos usuarios
class RegistroForm(UserCreationForm):
    """
    Formulario para el registro de un nuevo usuario. Extiende de UserCreationForm para manejar la creación de usuarios.
    """
    # Campo para el correo electrónico del usuario
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))

    class Meta:
        model = Usuario  # Especificamos el modelo a usar
        fields = ['email', 'username', 'password1', 'password2']  # Campos del formulario

# Formulario de inicio de sesión con correo electrónico y contraseña
class EmailLoginForm(AuthenticationForm):
    """
    Formulario para iniciar sesión con el correo electrónico del usuario.
    """
    # Campo para el correo electrónico
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))
    # Campo para la contraseña
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

# Formulario para la reserva de una cita
class ReservaForm(forms.ModelForm):
    """
    Formulario para la reserva de citas con un profesional. 
    Permite elegir un profesional, la fecha y la hora de la cita.
    """
    # Campo para seleccionar el profesional
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),  # Obtenemos todos los profesionales
        label="Selecciona un Profesional",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # Campo para la fecha de la cita
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Input de tipo fecha
        label="Fecha de la Cita"
    )
    # Campo para la hora de la cita
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),  # Input de tipo hora
        label="Hora de la Cita"
    )

    class Meta:
        model = Cita  # Modelo relacionado con este formulario
        fields = ['profesional', 'fecha', 'hora']  # Campos a incluir en el formulario

    def save(self, commit=True):
        """
        Sobrescribimos el método save para manejar el guardado del objeto Cita
        """
        cita = super().save(commit=False)  # Preparamos la cita, pero aún no la guardamos
        if commit:
            cita.save()  # Guardamos la cita si commit es True
        return cita

# Formulario para la creación de reseñas
class ReseñaForm(forms.ModelForm):
    """
    Formulario para que los usuarios dejen reseñas sobre los profesionales.
    Incluye una calificación y un comentario.
    """
    # Campo para la calificación (de 1 a 5)
    calificacion = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        label="Calificación (1-5)"
    )
    # Campo para el comentario
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario aquí...'}),
        label="Comentario"
    )

    class Meta:
        model = Reseña  # Modelo de reseña
        fields = ['calificacion', 'comentario']  # Campos que se incluyen en el formulario

# Formulario para crear o editar un profesional
class ProfesionalForm(forms.ModelForm):
    """
    Formulario para crear o editar el perfil de un profesional.
    Incluye campos como nombre, especialidad, biografía, etc.
    """
    class Meta:
        model = Profesional  # Modelo del profesional
        fields = ['nombre', 'especialidad', 'ubicacion', 'biografia', 'disponibilidad', 'correo', 'telefono', 'descripcion', 'foto']
        widgets = {
            'disponibilidad': forms.Textarea(attrs={'rows': 3}),  # Campo para la disponibilidad, con más filas
            'descripcion': forms.Textarea(attrs={'rows': 4}),  # Campo para la descripción, con más filas
        }

    def save(self, commit=True):
        """
        Sobrescribimos el método save para establecer el campo is_staff en True,
        de modo que el profesional sea considerado parte del personal del sistema.
        """
        profesional = super().save(commit=False)  # Creamos la instancia del profesional
        if commit:
            # Aquí accedemos al usuario asociado con el profesional y lo convertimos en 'staff'
            user = profesional.user  # Se asume que existe una relación entre Profesional y Usuario
            user.is_staff = True  # Establecemos que este usuario es parte del staff
            user.save()  # Guardamos los cambios del usuario
            profesional.save()  # Guardamos los cambios del profesional
        return profesional