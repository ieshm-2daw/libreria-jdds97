# Generated by Django 4.2.7 on 2023-12-18 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0019_alter_libro_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='genero',
            field=models.ManyToManyField(default=False, max_length=100, null=True, to='biblioteca.genero'),
        ),
    ]
