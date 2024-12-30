from django.contrib import admin
from .models import (
    Promocion, TipoDeEvento, Evento, Cliente, Alquiler, 
    FotoAlquiler, Servicio, FotoServicio, AlquilerServicio, 
    Administrador, Eventualidad
)


# Configuración para el modelo Promocion
@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('idpromocion', 'descripcion_promocion', 'valor_referencial_promo', 'estado_promocion', 'fecha_caducidad')
    search_fields = ('descripcion_promocion',)
    list_filter = ('estado_promocion', 'fecha_caducidad')

# Configuración para el modelo TipoDeEvento
@admin.register(TipoDeEvento)
class TipoDeEventoAdmin(admin.ModelAdmin):
    list_display = ('idTipo_De_Evento', 'nombre_evento', 'fecha_creacion')
    search_fields = ('nombre_evento',)
    list_filter = ('fecha_creacion',)

# Configuración para el modelo Evento
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('idevento', 'descripcion', 'valor_referencial', 'numero_horas_permitidas', 'tipo_de_evento')
    search_fields = ('descripcion',)
    list_filter = ('tipo_de_evento',)

# Configuración para el modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idcliente', 'nombres', 'apellidos', 'correo_electronico', 'telefono')
    search_fields = ('nombres', 'apellidos', 'correo_electronico')
    list_filter = ('nacionalidad', 'genero')

# Configuración para el modelo Alquiler
@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display = ('idalquiler', 'idcliente', 'idevento', 'fecha_alquiler', 'costo_alquiler', 'estado_de_alquiler')
    search_fields = ('idcliente__nombres', 'idevento__descripcion')
    list_filter = ('fecha_alquiler', 'estado_de_alquiler')

# Configuración para el modelo FotoAlquiler
@admin.register(FotoAlquiler)
class FotoAlquilerAdmin(admin.ModelAdmin):
    list_display = ('idFoto_Alquiler', 'idevento', 'url_foto', 'descripcion', 'likes', 'dislikes', 'fecha_subida')
    search_fields = ('descripcion',)
    list_filter = ('fecha_subida',)

# Configuración para el modelo Servicio
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('idservicio', 'descripcion_servicio', 'valor_unidad', 'estado_servicio', 'fecha_entrega')
    search_fields = ('descripcion_servicio',)
    list_filter = ('estado_servicio', 'fecha_entrega')

# Configuración para el modelo FotoServicio
@admin.register(FotoServicio)
class FotoServicioAdmin(admin.ModelAdmin):
    list_display = ('idfoto_servicio', 'idservicio', 'url_imagen', 'descripcion_foto', 'likes', 'dislikes', 'fecha_publicacion')
    search_fields = ('descripcion_foto',)
    list_filter = ('fecha_publicacion',)

# Configuración para el modelo AlquilerServicio
@admin.register(AlquilerServicio)
class AlquilerServicioAdmin(admin.ModelAdmin):
    list_display = ('idalquiler_servicio', 'idalquiler', 'idservicio', 'cantidad', 'costo_total', 'calificacion_cliente')
    search_fields = ('idalquiler__idcliente__nombres',)
    list_filter = ('costo_total',)

# Configuración para el modelo Administrador
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('idadmin', 'nombre_negocio', 'correo_negocio', 'telefono_negocio', 'numero_cuenta', 'banco')
    search_fields = ('nombre_negocio', 'correo_negocio')
    list_filter = ('banco',)

# Configuración para el modelo Eventualidad
@admin.register(Eventualidad)
class EventualidadAdmin(admin.ModelAdmin):
    list_display = ('ideventualidad', 'idalquiler', 'descripcion_eventualidad', 'fecha_eventualidad', 'tipo_eventualidad', 'costo_eventualidad', 'responsable', 'fecha_resolucion')
    search_fields = ('descripcion_eventualidad', 'responsable')
    list_filter = ('tipo_eventualidad', 'fecha_eventualidad')



