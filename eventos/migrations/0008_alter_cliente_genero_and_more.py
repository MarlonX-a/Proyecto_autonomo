# Generated by Django 5.1.3 on 2024-12-09 13:17

import eventos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0007_alter_fotoservicio_fecha_publicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=20),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='identificacion_cliente',
            field=models.CharField(max_length=10, unique=True, validators=[eventos.validators.validar_cedula], verbose_name='Identificación cliente'),
        ),
    ]
