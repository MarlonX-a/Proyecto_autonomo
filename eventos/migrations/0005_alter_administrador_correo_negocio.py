# Generated by Django 5.1.3 on 2024-12-03 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_alter_cliente_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrador',
            name='correo_negocio',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]