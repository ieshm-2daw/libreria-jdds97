from typing import Any
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Libro, Autor, Prestamo, Usuario
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


# pylint: disable=no-member
class Crear_libro(CreateView):
    model = Libro
    fields = "__all__"
    success_url = reverse_lazy("listar")


class Listar_libros(ListView):
    model = Libro
    """
    queryset=Libro.objects.filter(disponibilidad="D")

    """

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["libros_disponibles"] = Libro.objects.filter(disponibilidad="D")
        context["libros_reservados"] = Libro.objects.filter(disponibilidad="R")
        return context


class Editar_libro(UpdateView):
    model = Libro
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("listar")


class Eliminar_libro(DeleteView):
    model = Libro
    success_url = reverse_lazy("listar")


class Detalles_libro(DetailView):
    model = Libro


class Crear_autor(CreateView):
    model = Autor
    fields = "__all__"
    success_url = reverse_lazy("listar_autores")


class Libros_disponibles(ListView):
    model = Libro
    queryset = Libro.objects.filter(disponibilidad="D")
    template_name_suffix = "_disponibles"


class Mis_libros(ListView):
    model = Prestamo
    template_name_suffix = "_mios"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["libros_devueltos"] = Prestamo.objects.filter(
            usuario=self.request.user, estado="D"
        )
        context["libros_prestados"] = Prestamo.objects.filter(
            usuario=self.request.user, estado="P"
        )
        return context


# Arreglar prestamo para el usuario
class Crear_prestamo(CreateView):
    model = Prestamo
    success_url = reverse_lazy("listar")

    def get(self, request, *args, **kwargs):
        libro = Libro.objects.get(pk=self.kwargs["pk"])
        prestamo = Prestamo.objects.get(
            libro=libro,
            usuario=self.request.user,
        )
        prestamo.save()
        libro.disponibilidad = "P"
        libro.save()
        return redirect(self.get_success_url())


class Devolver_Libro(View):
    def post(self):
        libro = get_object_or_404(Libro, pk=self.kwargs["pk"])
        prestamo = get_object_or_404(
            Prestamo, usuario=self.request.user, estado="P", libro=libro
        )
        prestamo.estado = "D"
        prestamo.save()
        libro.disponibilidad = "P"
        libro.save()
        return redirect("listar")


# Editar mañana
class Buscar_Libro(ListView):
    model = Libro
    template_name_suffix = "_buscar"

    def get_queryset(self):
        titulo = self.request.GET.get("titulo")
        return Libro.objects.filter(titulo__icontains=titulo)
