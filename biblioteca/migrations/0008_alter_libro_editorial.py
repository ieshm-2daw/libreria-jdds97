# Generated by Django 4.2.7 on 2023-11-28 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0007_rename_author_autor_prestamo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='editorial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biblioteca.editorial'),
        ),
    ]