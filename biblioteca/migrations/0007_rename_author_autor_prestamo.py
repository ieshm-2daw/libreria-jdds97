# Generated by Django 4.2.7 on 2023-11-28 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0006_alter_usuario_telefono'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Author',
            new_name='Autor',
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_prestamo', models.DateField()),
                ('fecha_devolucion', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('P', 'Prestado'), ('D', 'Devuelto')], default='P', max_length=20)),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.libro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
