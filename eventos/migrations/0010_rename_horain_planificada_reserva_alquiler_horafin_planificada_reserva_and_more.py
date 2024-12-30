# Generated by Django 5.1.3 on 2024-12-09 14:15

import eventos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0009_alter_cliente_telefono'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alquiler',
            old_name='horain_planificada_reserva',
            new_name='horafin_planificada_reserva',
        ),
        migrations.AlterField(
            model_name='administrador',
            name='telefono_negocio',
            field=models.CharField(max_length=15, validators=[eventos.validators.validar_numero_celular], verbose_name='Número de celular'),
        ),
        migrations.AlterField(
            model_name='alquiler',
            name='estado_de_alquiler',
            field=models.CharField(choices=[('D', 'Disponible'), ('R', 'Reservado'), ('O', 'Ocupado'), ('F', 'Finalizado')], max_length=30),
        ),
        migrations.AlterField(
            model_name='promocion',
            name='estado_promocion',
            field=models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], max_length=20),
        ),
        migrations.AlterField(
            model_name='tipodeevento',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]