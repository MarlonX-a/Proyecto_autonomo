from .models import Administrador

def nombre_negocio(request):
    try:
        administrador = Administrador.objects.first()  # Obtener el único registro de Administrador
        return {'nombre_negocio': administrador.nombre_negocio if administrador else 'Mi Aplicación'}
    except Administrador.DoesNotExist:
        return {'nombre_negocio': 'Mi Aplicación'}
    
def administrador_data(request):
    try:
        administrador = Administrador.objects.first()  # Obtén el primer administrador (ajusta si es necesario)
        return {
            'administrador': administrador  # Esta variable estará disponible en todas las plantillas
        }
    except Administrador.DoesNotExist:
        return {
            'administrador': None  # Si no hay ningún administrador, se retorna None
        }