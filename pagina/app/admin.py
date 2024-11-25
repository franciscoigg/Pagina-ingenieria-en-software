from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Profesional, Cita, Usuario

# Define un Inline para mostrar las citas dentro del perfil del profesional
class CitaInline(admin.TabularInline):
    model = Cita
    extra = 0  # No agregar citas vacías
    fields = ['paciente', 'fecha', 'hora', 'estado']  # Qué campos mostrar
    readonly_fields = ['paciente', 'fecha', 'hora', 'estado']  # Solo lectura

# Admin para el modelo Profesional
@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'ubicacion', 'biografia', 'correo', 'telefono')
    inlines = [CitaInline]  # Añade el inline para mostrar las citas asociadas
    search_fields = ['nombre', 'especialidad', 'ubicacion', 'correo']  # Permite buscar por nombre, especialidad, etc.
    list_filter = ('especialidad', 'ubicacion')  # Filtrado por especialidad o ubicación

# Admin para el modelo Cita
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'profesional', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'profesional')  # Filtrar por estado o profesional
    search_fields = ['paciente__username', 'profesional__nombre', 'fecha']  # Permite búsqueda por nombre de paciente, profesional y fecha

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:  # Si el usuario es un profesional (staff)
            return queryset.filter(profesional__user=request.user)  # Solo las citas del profesional autenticado
        return queryset

# Registrar los modelos en Django Admin
admin.site.register(Cita, CitaAdmin)


class CustomUserAdmin(UserAdmin):
    # Aquí se define qué campos mostrar en el formulario de edición de un usuario.
    model = Usuario
    list_display = ['email', 'username', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['date_joined']

    # Los campos que quieres que se muestren en el formulario de usuario
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'is_staff', 'is_active')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    # Para agregar los campos en el formulario de edición
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

# Registramos el modelo con nuestro admin personalizado
admin.site.register(Usuario, CustomUserAdmin)