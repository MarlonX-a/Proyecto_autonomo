from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ClienteForm, EventoForm, PromocionForm, TipoDeEventoForm, AlquilerForm, FotoAlquilerForm, ServicioForm, FotoServicioForm, AlquilerServicioForm, AdministradorForm, EventualidadForm 
from .models import Evento, Alquiler, Promocion, TipoDeEvento, Cliente, FotoAlquiler, Servicio, FotoServicio, AlquilerServicio, Administrador, Eventualidad
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm #
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def is_usuario(user):
    return user.groups.filter(name="Usuario").exists()

def is_dueno(user):
    return user.groups.filter(name="Dueño de Negocio").exists()

def is_admin(user):
    return user.groups.filter(name="Administrador").exists()



def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': request.build_absolute_uri('/')[:-1],  # Construye el dominio absoluto
                        'site_name': 'Mi Sitio Web',  # Cambia esto por el nombre de tu sitio
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',  # Usa 'https' si tu sitio usa HTTPS
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, 'marlonalvime05@gmail.com', [user.email], fail_silently=False)  # Cambia 'marlonalvime05@gmail.com' por tu correo
                return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset_form.html", context={"password_reset_form": password_reset_form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda al usuario

            grupo = Group.objects.get(name="Usuario")
            user.groups.add(grupo)

            try:
                # URL para completar la información del cliente
                completar_cliente_url = request.build_absolute_uri(
                    reverse('completar_cliente', kwargs={'user_id': user.id})
                )
                
                # Enviar correo con el enlace
                send_mail(
                    'Bienvenido a Nuestro Sistema de Eventos Sociales',
                    f'Hola {user.username}, gracias por registrarte.\n\n'
                    f'Por favor completa tu información como cliente en el siguiente enlace:\n'
                    f'{completar_cliente_url}',
                    'marlonalvime05@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                return redirect('login')  # Redirige al login después de registrar al usuario
            except Exception as e:
                print(f"Error al enviar correo: {e}")
                return redirect('login')  # Redirige al register en caso de error
    else:
        form = CustomUserCreationForm()  # Formulario de registro de usuario
    return render(request, 'register.html', {'form': form})




def home_view(request): 
    eventos = Evento.objects.all()
    servicios = Servicio.objects.all()
    promociones = Promocion.objects.all()
    return render(request, 'home.html', {
        'eventos': eventos,
        'servicios': servicios,
        'promociones': promociones,
    })


@login_required
@user_passes_test(is_usuario)
def evento_list(request):
    eventos = Evento.objects.all()
    context = {
        'eventos': eventos,
        'is_usuario': is_usuario(request.user),
        'is_dueno': is_dueno(request.user),
        'is_admin': is_admin(request.user),
    }
    return render(request, 'evento_list.html', context)

@login_required
@user_passes_test(is_dueno)
def evento_create(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('evento_list')  # Redirige a la lista de eventos
    else:
        form = EventoForm()
    return render(request, 'evento_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def evento_update(request, idevento):
    evento = get_object_or_404(Evento, idevento=idevento)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('evento_list')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'evento_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def evento_delete(request, idevento):
    evento = get_object_or_404(Evento, idevento=idevento)
    if request.method == 'POST':
        evento.delete()
        return redirect('evento_list')
    return render(request, 'evento_confirm_delete.html', {'evento': evento})

@login_required
@user_passes_test(is_dueno)
def reportes(request):
    alquileres_por_mes = (
        Alquiler.objects
        .annotate(mes=ExtractMonth('fecha_alquiler'), anio=ExtractYear('fecha_alquiler'))
        .values('mes', 'anio')
        .annotate(cantidad=Count('idalquiler'))  # Cambié id_alquiler por idalquiler
        .order_by('anio', 'mes')
    )

    ganancias_por_mes = (
        Alquiler.objects
        .annotate(mes=ExtractMonth('fecha_alquiler'), anio=ExtractYear('fecha_alquiler'))
        .values('mes', 'anio')
        .annotate(ganancias=Sum('costo_alquiler'))  # Asegúrate de que 'costo_alquiler' sea el nombre correcto
        .order_by('anio', 'mes')
    )

    clientes_frecuentes = (
        Alquiler.objects
        .values('idcliente__nombres')  # Cambié cliente__nombres a idcliente__nombres
        .annotate(cantidad=Count('idalquiler'))  # Cambié id_alquiler por idalquiler
        .order_by('-cantidad')[:5]
    )

    # Generación del gráfico
    buffer = io.BytesIO()
    plt.figure(figsize=(10, 6))
    meses = [f"{item['mes']}/{item['anio']}" for item in alquileres_por_mes]
    cantidades = [item['cantidad'] for item in alquileres_por_mes]
    plt.bar(meses, cantidades, color='skyblue')
    plt.title('Cantidad de Alquileres por Mes')
    plt.xlabel('Mes/Año')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, 'reportes.html', {
        'imagen_base64': imagen_base64,
        'clientes_frecuentes': clientes_frecuentes,
        'ganancias_por_mes': ganancias_por_mes,
    })

@login_required
# Vista para listar las promociones
@user_passes_test(is_dueno)
def promocion_list(request):
    promociones = Promocion.objects.all()
    return render(request, 'promocion_list.html', {'promociones': promociones})

@login_required
# Vista para crear una nueva promoción
@user_passes_test(is_dueno)
def promocion_create(request):
    if request.method == 'POST':
        form = PromocionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promocion_list')  # Redirige a la lista de promociones después de guardar
    else:
        form = PromocionForm()
    return render(request, 'promocion_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
# Vista para actualizar una promoción existente
def promocion_update(request, idpromocion):
    promocion = get_object_or_404(Promocion, idpromocion=idpromocion)
    if request.method == 'POST':
        form = PromocionForm(request.POST, instance=promocion)
        if form.is_valid():
            form.save()
            return redirect('promocion_list')  # Redirige a la lista de promociones después de actualizar
    else:
        form = PromocionForm(instance=promocion)
    return render(request, 'promocion_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
# Vista para eliminar una promoción
def promocion_delete(request, idpromocion):
    promocion = get_object_or_404(Promocion, idpromocion=idpromocion)
    if request.method == 'POST':
        promocion.delete()
        return redirect('promocion_list')  # Redirige a la lista de promociones después de eliminar
    return render(request, 'promocion_confirm_delete.html', {'promocion': promocion})


@login_required
def completar_cliente(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Recupera el usuario por ID
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = user  # Asocia el usuario con el cliente
            cliente.correo_electronico = user.email
            cliente.save()
            return redirect('login')
    else:
        form = ClienteForm()  # Formulario para completar la información
    return render(request, 'completar_cliente.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_dueno)
# Vista para listar los tipos de evento
def tipoevento_list(request):
    tipos_evento = TipoDeEvento.objects.all()
    return render(request, "tipoevento_list.html", {"tipos_evento": tipos_evento})

@login_required
@user_passes_test(is_dueno)
# Vista para crear un nuevo tipo de evento
def tipoevento_create(request):
    if request.method == "POST":
        form = TipoDeEventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("tipoevento_list")
    else:
        form = TipoDeEventoForm()
    return render(request, "tipoevento_form.html", {"form": form})

@login_required
@user_passes_test(is_dueno)
# Vista para actualizar un tipo de evento
def tipoevento_update(request, pk):
    tipo_evento = get_object_or_404(TipoDeEvento, pk=pk)
    if request.method == "POST":
        form = TipoDeEventoForm(request.POST, request.FILES, instance=tipo_evento)
        if form.is_valid():
            form.save()
            return redirect("tipoevento_list")
    else:
        form = TipoDeEventoForm(instance=tipo_evento)
    return render(request, "tipoevento_form.html", {"form": form})

@login_required
# Vista para eliminar un tipo de evento
@user_passes_test(is_dueno)
def tipoevento_delete(request, pk):
    tipo_evento = get_object_or_404(TipoDeEvento, pk=pk)
    if request.method == "POST":
        tipo_evento.delete()
        return redirect("tipoevento_list")
    return render(request, "tipoevento_confirm_delete.html", {"tipo_evento": tipo_evento})

@login_required
# Vista para listar todas las eventualidades
@user_passes_test(is_dueno)
def eventualidad_list(request):
    eventualidades = Eventualidad.objects.all()
    return render(request, "eventualidad_list.html", {"eventualidades": eventualidades})

@login_required
@user_passes_test(is_dueno)
# Vista para crear una nueva eventualidad
def eventualidad_create(request):
    if request.method == "POST":
        form = EventualidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("eventualidad_list")
    else:
        form = EventualidadForm()
    return render(request, "eventualidad_form.html", {"form": form})

@login_required
@user_passes_test(is_dueno)
# Vista para editar una eventualidad existente
def eventualidad_update(request, pk):
    eventualidad = get_object_or_404(Eventualidad, pk=pk)
    if request.method == "POST":
        form = EventualidadForm(request.POST, instance=eventualidad)
        if form.is_valid():
            form.save()
            return redirect("eventualidad_list")
    else:
        form = EventualidadForm(instance=eventualidad)
    return render(request, "eventualidad_form.html", {"form": form})

@login_required
@user_passes_test(is_dueno)
# Vista para eliminar una eventualidad
def eventualidad_delete(request, pk):
    eventualidad = get_object_or_404(Eventualidad, pk=pk)
    if request.method == "POST":
        eventualidad.delete()
        return redirect("eventualidad_list")
    return render(request, "eventualidad_confirm_delete.html", {"eventualidad": eventualidad})


@login_required
# Vista para listar todos los administradores
@user_passes_test(is_admin)
def administrador_list(request):
    administradores = Administrador.objects.all()
    return render(request, "administrador_list.html", {"administradores": administradores})

@login_required
@user_passes_test(is_admin)
# Vista para crear un nuevo administrador
def administrador_create(request):
    if request.method == "POST":
        # Aquí pasamos 'request.FILES' para manejar los archivos subidos, como las imágenes
        form = AdministradorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("administrador_list")  # Redirige a la lista de administradores después de guardar
    else:
        form = AdministradorForm()  # Si no es un POST, simplemente mostramos un formulario vacío

    return render(request, "administrador_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
# Vista para editar un administrador existente
def administrador_update(request, pk):
    administrador = get_object_or_404(Administrador, pk=pk)
    if request.method == "POST":
        form = AdministradorForm(request.POST, request.FILES, instance=administrador)  # Asegúrate de pasar request.FILES
        if form.is_valid():
            form.save()
            return redirect("administrador_list")
    else:
        form = AdministradorForm(instance=administrador)
    return render(request, "administrador_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
# Vista para eliminar un administrador
def administrador_delete(request, pk):
    administrador = get_object_or_404(Administrador, pk=pk)
    if request.method == "POST":
        administrador.delete()
        return redirect("administrador_list")
    return render(request, "administrador_confirm_delete.html", {"administrador": administrador})


@login_required
# Vista para listar los alquileres
def alquiler_list(request):
    alquileres = Alquiler.objects.all()
    return render(request, "alquiler_list.html", {"alquileres": alquileres})

@login_required
# Vista para crear un nuevo alquiler
def alquiler_create(request):
    if request.method == "POST":
        form = AlquilerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("alquiler_list")
    else:
        form = AlquilerForm()
    return render(request, "alquiler_form.html", {"form": form})

@login_required
# Vista para actualizar un alquiler existente
def alquiler_update(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk)
    if request.method == "POST":
        form = AlquilerForm(request.POST, instance=alquiler)
        if form.is_valid():
            form.save()
            return redirect("alquiler_list")
    else:
        form = AlquilerForm(instance=alquiler)
    return render(request, "alquiler_form.html", {"form": form})

@login_required
# Vista para eliminar un alquiler
def alquiler_delete(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk)
    if request.method == "POST":
        alquiler.delete()
        return redirect("alquiler_list")
    return render(request, "alquiler_confirm_delete.html", {"alquiler": alquiler})



@login_required
def listar_fotos_alquiler(request):
    fotos = FotoAlquiler.objects.all()
    return render(request, 'fotos_alquiler_list.html', {'fotos': fotos})

@login_required
@user_passes_test(is_dueno)
def crear_foto_alquiler(request):
    if request.method == 'POST':
        form = FotoAlquilerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_fotos_alquiler')
    else:
        form = FotoAlquilerForm()
    return render(request, 'fotos_alquiler_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def editar_foto_alquiler(request, id_foto):
    foto = get_object_or_404(FotoAlquiler, pk=id_foto)
    if request.method == 'POST':
        form = FotoAlquilerForm(request.POST, request.FILES, instance=foto)
        if form.is_valid():
            form.save()
            return redirect('listar_fotos_alquiler')
    else:
        form = FotoAlquilerForm(instance=foto)
    return render(request, 'fotos_alquiler_form.html', {'form': form, 'foto': foto})

@login_required
@user_passes_test(is_dueno)
def eliminar_foto_alquiler(request, id_foto):
    foto = get_object_or_404(FotoAlquiler, pk=id_foto)
    if request.method == 'POST':
        foto.delete()
        return redirect('listar_fotos_alquiler')
    return render(request, 'fotos_alquiler_confirm_delete.html', {'foto': foto})


@login_required
@user_passes_test(is_dueno)
def servicio_list(request):
    servicios = Servicio.objects.all()  # Obtener todos los servicios
    return render(request, 'servicio_list.html', {'servicios': servicios})

@login_required
@user_passes_test(is_dueno)
def servicio_create(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo servicio
            return redirect('servicio_list')  # Redirige a la lista de servicios
    else:
        form = ServicioForm()
    return render(request, 'servicio_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def servicio_edit(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()  # Actualiza el servicio
            return redirect('servicio_list')  # Redirige a la lista de servicios
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'servicio_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()  # Elimina el servicio
        return redirect('servicio_list')  # Redirige a la lista de servicios
    return render(request, 'servicio_confirm_delete.html', {'servicio': servicio})


@login_required
@user_passes_test(is_dueno)
def foto_servicio_list(request):
    fotos_servicio = FotoServicio.objects.all()  # Obtener todas las fotos de servicio
    return render(request, 'foto_servicio_list.html', {'fotos_servicio': fotos_servicio})

@login_required
@user_passes_test(is_dueno)
def foto_servicio_create(request):
    if request.method == 'POST':
        form = FotoServicioForm(request.POST, request.FILES)  # Incluye request.FILES para subir imágenes
        if form.is_valid():
            form.save()  # Guarda la nueva foto de servicio
            return redirect('foto_servicio_list')  # Redirige a la lista de fotos de servicio
    else:
        form = FotoServicioForm()
    return render(request, 'foto_servicio_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def foto_servicio_edit(request, pk):
    foto_servicio = get_object_or_404(FotoServicio, pk=pk)
    if request.method == 'POST':
        form = FotoServicioForm(request.POST, request.FILES, instance=foto_servicio)  # Edita la foto
        if form.is_valid():
            form.save()  # Actualiza la foto de servicio
            return redirect('foto_servicio_list')  # Redirige a la lista de fotos de servicio
    else:
        form = FotoServicioForm(instance=foto_servicio)
    return render(request, 'foto_servicio_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def foto_servicio_delete(request, pk):
    foto_servicio = get_object_or_404(FotoServicio, pk=pk)
    if request.method == 'POST':
        foto_servicio.delete()  # Elimina la foto de servicio
        return redirect('foto_servicio_list')  # Redirige a la lista de fotos de servicio
    return render(request, 'foto_servicio_confirm_delete.html', {'foto_servicio': foto_servicio})

@login_required
@user_passes_test(is_dueno)
def alquiler_servicio_list(request):
    alquiler_servicios = AlquilerServicio.objects.all()
    return render(request, 'alquiler_servicio_list.html', {'alquiler_servicios': alquiler_servicios})

@login_required
@user_passes_test(is_dueno)
def alquiler_servicio_create(request):
    if request.method == 'POST':
        form = AlquilerServicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('alquiler_servicio_list')
    else:
        form = AlquilerServicioForm()
    return render(request, 'alquiler_servicio_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def alquiler_servicio_update(request, pk):
    alquiler_servicio = get_object_or_404(AlquilerServicio, pk=pk)
    if request.method == 'POST':
        form = AlquilerServicioForm(request.POST, request.FILES, instance=alquiler_servicio)
        if form.is_valid():
            form.save()
            return redirect('alquiler_servicio_list')
    else:
        form = AlquilerServicioForm(instance=alquiler_servicio)
    return render(request, 'alquiler_servicio_form.html', {'form': form})

@login_required
@user_passes_test(is_dueno)
def alquiler_servicio_delete(request, pk):
    alquiler_servicio = get_object_or_404(AlquilerServicio, pk=pk)
    if request.method == 'POST':
        alquiler_servicio.delete()
        return redirect('alquiler_servicio_list')
    return render(request, 'alquiler_servicio_confirm_delete.html', {'alquiler_servicio': alquiler_servicio})

def custom_page_not_found(request, exception):
    return render(request, '404.html', {}, status=404)



@login_required
def evento_detalle(request, idevento):
    try:
        # Intenta obtener el evento correspondiente al ID
        evento = Evento.objects.get(idevento=idevento)
    except Evento.DoesNotExist:
        # Si no existe un evento con ese ID, puedes redirigir a una página de error o mostrar un mensaje
        return render(request, 'evento_no_encontrado.html')  # Plantilla de error, si no se encuentra el evento

    # Si el evento se encuentra correctamente, lo pasas a la plantilla
    return render(request, 'evento_detalle.html', {'evento': evento})