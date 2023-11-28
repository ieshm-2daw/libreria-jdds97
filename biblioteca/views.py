from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from .models import Libro,Autor


class Crear_libro(CreateView):
    model=Libro
    fields = ['titulo','autor','editorial','fecha_publicacion','rating']
    success_url = reverse_lazy("listar")
    
class Listar_libros(ListView):
    model=Libro
class Editar_libro(UpdateView):
    model=Libro
    template_name_suffix='_update_form'
class Eliminar_libro(DeleteView):
    model=Libro
    success_url = reverse_lazy("listar")
class Detalles_libro(DetailView):
    model=Libro
class Crear_autor(CreateView):
    model=Autor
    fields="__all__"
    success_url=reverse_lazy("listar_autores")