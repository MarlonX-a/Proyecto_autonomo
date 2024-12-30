from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea grupos de usuario predeterminados'

    def handle(self, *args, **kwargs):
        grupos = ['Usuario', 'Dueño de Negocio', 'Administrador']
        for nombre in grupos:
            group, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(f"Grupo '{nombre}' creado.")
            else:
                self.stdout.write(f"Grupo '{nombre}' ya existe.")
