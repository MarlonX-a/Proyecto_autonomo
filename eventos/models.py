from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from .validators import validar_cedula, validar_numero_celular

class Promocion(models.Model):
    idpromocion = models.AutoField(primary_key=True)
    descripcion_promocion = models.CharField(max_length=100)
    valor_referencial_promo = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_promocion = models.CharField(max_length=100)
    porcentaje_promocion = models.IntegerField()
    fecha_vigencia = models.DateField()
    fecha_caducidad = models.DateField()
    estado_promocion = models.CharField(max_length=20, choices=[('A', 'Activo'),('I', 'Inactivo')])

class TipoDeEvento(models.Model):
    idTipo_De_Evento = models.AutoField(primary_key=True)
    nombre_evento = models.CharField(max_length=50)
    url_imagen = CloudinaryField('image')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_evento


class Evento(models.Model):
    idevento = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    valor_referencial = models.DecimalField(max_digits=10, decimal_places=2)
    numero_horas_permitidas = models.IntegerField()
    valor_extra_hora = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_de_evento = models.ForeignKey(TipoDeEvento, on_delete=models.CASCADE, related_name="eventos")

    def __str__(self):
        return f"{self.tipo_de_evento.nombre_evento} - {self.descripcion[:30]}"


class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    identificacion_cliente = models.CharField(
        max_length=10,
        validators=[validar_cedula],  # Validador para cédula
        unique=True,
        verbose_name="Identificación cliente"
    )
    nacionalidad = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)  # Fecha automática
    telefono = models.CharField(
        max_length=10,  # Máximo 10 caracteres
        validators=[validar_numero_celular],  # Validador personalizado para celular
        verbose_name="Número de celular"
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    genero = models.CharField(
        max_length=20,
        choices=[
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('O', 'Otro')
        ]
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')  # Relación con User

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Alquiler(models.Model):
    idalquiler = models.AutoField(primary_key=True)
    idcliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="alquileres")
    idevento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="alquileres")
    fecha_alquiler = models.DateField()
    horainicio_reserva = models.TimeField()
    horafin_planificada_reserva = models.TimeField()
    horafin_real_reserva = models.TimeField()
    costo_alquiler = models.DecimalField(max_digits=10, decimal_places=2)
    calificacion_negocio = models.IntegerField()
    observacion = models.TextField()
    cantidad_anticipo = models.DecimalField(max_digits=10, decimal_places=2)
    estado_de_alquiler = models.CharField(max_length=30, choices=[('R', 'Reservado'),('O', 'Ocupado'), ('F', 'Finalizado')])

    def __str__(self):
        return f"Alquiler #{self.idalquiler}"

class FotoAlquiler(models.Model):
    idFoto_Alquiler = models.AutoField(primary_key=True)
    idevento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="fotos_alquiler")
    url_foto = CloudinaryField('image')
    descripcion = models.CharField(max_length=200)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class Servicio(models.Model):
    idservicio = models.AutoField(primary_key=True)
    descripcion_servicio = models.CharField(max_length=150)
    valor_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    estado_servicio = models.CharField(max_length=100)
    fecha_entrega = models.DateTimeField()
    descripcion_unidad = models.CharField(max_length=200)
    fecha_actualizacion_precio = models.DateTimeField()

    def __str__(self):
        return f"{self.idservicio} - {self.descripcion_servicio}"

class FotoServicio(models.Model):
    idfoto_servicio = models.AutoField(primary_key=True)
    idservicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="fotos")
    url_imagen = CloudinaryField('image')
    descripcion_foto = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


class AlquilerServicio(models.Model):
    idalquiler_servicio = models.AutoField(primary_key=True)
    idalquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE, related_name="servicios")
    idservicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="alquileres")
    cantidad = models.IntegerField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    calificacion_cliente = models.IntegerField()

class Administrador(models.Model):
    idadmin = models.AutoField(primary_key=True)
    nombre_negocio = models.CharField(max_length=100)
    direccion_negocio = models.CharField(max_length=150)
    correo_negocio = models.EmailField(unique=True)
    telefono_negocio = models.CharField(max_length=15, validators=[validar_numero_celular], verbose_name="Número de celular")
    pagina_web = models.CharField(max_length=100)
    facebook_negocio = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50)
    tipo_cuenta = models.CharField(max_length=30)
    banco = models.CharField(max_length=50)
    logo = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.nombre_negocio

class Eventualidad(models.Model):
    ideventualidad = models.AutoField(primary_key=True)
    idalquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE, related_name="eventualidades")
    descripcion_eventualidad = models.CharField(max_length=200)
    fecha_eventualidad = models.DateField()
    tipo_eventualidad = models.CharField(max_length=20)
    costo_eventualidad = models.DecimalField(max_digits=10, decimal_places=2)
    responsable = models.CharField(max_length=100)
    fecha_resolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.descripcion_eventualidad
