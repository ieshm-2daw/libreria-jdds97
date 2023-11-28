from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario,Libro,Autor,Editorial,Prestamo

admin.site.register(Usuario, UserAdmin)
admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Prestamo)
# Register your models here.
