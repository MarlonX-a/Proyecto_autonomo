# Generated by Django 5.1.3 on 2024-12-10 22:19

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0011_alter_alquiler_estado_de_alquiler'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrador',
            name='logo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
