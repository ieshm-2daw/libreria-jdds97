# Generated by Django 4.2.7 on 2023-11-28 09:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0005_alter_libro_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(9)]),
        ),
    ]
