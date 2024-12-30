from django import forms
from .models import (
    Promocion, TipoDeEvento, Evento, Cliente, Alquiler,
    FotoAlquiler, Servicio, FotoServicio, AlquilerServicio,
    Administrador, Eventualidad
)
from cloudinary.forms import CloudinaryFileField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),  # Estiliza el campo
        help_text=""  # Elimina el texto de ayuda del campo email
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="",  # Elimina el texto de ayuda predeterminado
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="",  # Elimina el texto de ayuda predeterminado
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email
    
    
# Formulario para Promocion
class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = '__all__'
        widgets = {
            "fecha_vigencia": forms.DateInput(attrs={"type": "date"}),
            "fecha_caducidad": forms.DateInput(attrs={"type": "date"}),
        }

# Formulario para TipoDeEvento
class TipoDeEventoForm(forms.ModelForm):
    class Meta:
        model = TipoDeEvento
        fields = '__all__'

# Formulario para Evento
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'

# Formulario para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['usuario', 'correo_electronico']

# Formulario para Alquiler
class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = '__all__'
        widgets = {
            "fecha_alquiler": forms.DateInput(attrs={"type": "date"}),
            "horainicio_reserva": forms.TimeInput(attrs={"type": "time"}),
            "horafin_planificada_reserva": forms.TimeInput(attrs={"type": "time"}),
            "horafin_real_reserva": forms.TimeInput(attrs={"type": "time"}),
        }

# Formulario para FotoAlquiler
class FotoAlquilerForm(forms.ModelForm):
    class Meta:
        model = FotoAlquiler
        fields = ['idevento', 'url_foto', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la foto'})
        }

# Formulario para Servicio
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {
            'descripcion_servicio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción del servicio'}),
            "fecha_entrega": forms.DateInput(attrs={"type": "date"}),
            'descripcion_unidad': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la foto'}),
            "fecha_actualizacion_precio": forms.DateInput(attrs={"type": "date"}),
        }

# Formulario para FotoServicio
class FotoServicioForm(forms.ModelForm):
    class Meta:
        model = FotoServicio
        fields = ['idservicio', 'url_imagen', 'descripcion_foto']
        widgets = {
            'descripcion_foto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la foto del servicio'})
        }

# Formulario para AlquilerServicio
class AlquilerServicioForm(forms.ModelForm):
    class Meta:
        model = AlquilerServicio
        fields = '__all__'

# Formulario para Administrador
class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = '__all__'

# Formulario para Eventualidad
class EventualidadForm(forms.ModelForm):
    class Meta:
        model = Eventualidad
        fields = '__all__'
        widgets = {
            'descripcion_eventualidad': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la eventualidad'}),
            "fecha_eventualidad": forms.DateInput(attrs={"type": "date"}),
            "fecha_resolucion": forms.DateInput(attrs={"type": "date"}),
        }



