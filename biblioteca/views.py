from typing import Any
from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from .models import Libro,Autor


class Crear_libro(CreateView):
    model=Libro
    fields = "__all__"
    success_url = reverse_lazy("listar")
    
class Listar_libros(ListView):
    model=Libro
    '''
    queryset=Libro.objects.filter(disponibilidad="D")

    '''
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad="D")
        context['libros_reservados'] = Libro.objects.filter(disponibilidad="R")
        return context
        
        
    
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
    