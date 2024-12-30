"""
URL configuration for centro_de_eventos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eventos import views # Importa la vista register_view
from django.contrib.auth.views import LoginView  # Importa LoginView para la autenticación
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('eventos/', views.evento_list, name='evento_list'),
    path('eventos/new/', views.evento_create, name='evento_create'),
    path('eventos/<int:idevento>/edit/', views.evento_update, name='evento_update'),
    path('eventos/<int:idevento>/delete/', views.evento_delete, name='evento_delete'),
    path('reportes/', views.reportes, name='reportes'),
    path('completar-cliente/<int:user_id>/', views.completar_cliente, name='completar_cliente'),
    path('promociones/', views.promocion_list, name='promocion_list'), 
    path('promocion/crear/', views.promocion_create, name='promocion_create'), 
    path('promocion/<int:idpromocion>/editar/', views.promocion_update, name='promocion_update'),
    path('promocion/<int:idpromocion>/eliminar/', views.promocion_delete, name='promocion_delete'),
    path("tipoevento/", views.tipoevento_list, name="tipoevento_list"),
    path("tipoevento/nuevo/", views.tipoevento_create, name="tipoevento_create"),
    path("tipoevento/editar/<int:pk>/", views.tipoevento_update, name="tipoevento_update"),
    path("tipoevento/eliminar/<int:pk>/", views.tipoevento_delete, name="tipoevento_delete"),
    path("eventualidades/", views.eventualidad_list, name="eventualidad_list"),
    path("eventualidades/nueva/", views.eventualidad_create, name="eventualidad_create"),
    path("eventualidades/editar/<int:pk>/", views.eventualidad_update, name="eventualidad_update"),
    path("eventualidades/eliminar/<int:pk>/", views.eventualidad_delete, name="eventualidad_delete"),
    path("administradores/", views.administrador_list, name="administrador_list"),
    path("administradores/nuevo/", views.administrador_create, name="administrador_create"),
    path("administradores/editar/<int:pk>/", views.administrador_update, name="administrador_update"),
    path("administradores/eliminar/<int:pk>/", views.administrador_delete, name="administrador_delete"),
    path("alquileres/", views.alquiler_list, name="alquiler_list"),
    path("alquileres/nuevo/", views.alquiler_create, name="alquiler_create"),
    path("alquileres/editar/<int:pk>/", views.alquiler_update, name="alquiler_update"),
    path("alquileres/eliminar/<int:pk>/", views.alquiler_delete, name="alquiler_delete"),
    path('fotos-alquiler/', views.listar_fotos_alquiler, name='listar_fotos_alquiler'),
    path('fotos-alquiler/nueva/', views.crear_foto_alquiler, name='crear_foto_alquiler'),
    path('fotos-alquiler/editar/<int:id_foto>/', views.editar_foto_alquiler, name='editar_foto_alquiler'),
    path('fotos-alquiler/eliminar/<int:id_foto>/', views.eliminar_foto_alquiler, name='eliminar_foto_alquiler'),
    path('servicios/', views.servicio_list, name='servicio_list'),
    path('servicios/crear/', views.servicio_create, name='servicio_create'),
    path('servicios/editar/<int:pk>/', views.servicio_edit, name='servicio_edit'),
    path('servicios/eliminar/<int:pk>/', views.servicio_delete, name='servicio_delete'),
    path('fotos-servicio/', views.foto_servicio_list, name='foto_servicio_list'),
    path('fotos-sevicio/crear/', views.foto_servicio_create, name='foto_servicio_create'),
    path('fotos-servicio/editar/<int:pk>/', views.foto_servicio_edit, name='foto_servicio_edit'),
    path('fotos-servicio/eliminar/<int:pk>/', views.foto_servicio_delete, name='foto_servicio_delete'),
    path('alquiler_servicios/', views.alquiler_servicio_list, name='alquiler_servicio_list'),
    path('alquiler_servicio/create/', views.alquiler_servicio_create, name='alquiler_servicio_create'),
    path('alquiler_servicio/<int:pk>/update/', views.alquiler_servicio_update, name='alquiler_servicio_update'),
    path('alquiler_servicio/<int:pk>/delete/', views.alquiler_servicio_delete, name='alquiler_servicio_delete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('evento/<int:idevento>/', views.evento_detalle, name='evento_detalle'),


    path('password_reset/', views.password_reset_request, name='recuperar_contrasenia'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

handler404 = 'eventos.views.custom_page_not_found'
