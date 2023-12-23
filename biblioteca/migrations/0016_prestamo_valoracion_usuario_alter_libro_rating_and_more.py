# Generated by Django 4.2.7 on 2023-12-17 21:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0015_alter_libro_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='valoracion_usuario',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='libro',
            name='rating',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.DeleteModel(
            name='Valoracion',
        ),
    ]