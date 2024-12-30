import os
import django

# Configura Django (necesario para que el ORM funcione)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

# Ahora puedes importar los modelos
from django.contrib.auth.models import User

# Crear el superusuario
user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
user.save()

print("Superusuario creado con éxito.")