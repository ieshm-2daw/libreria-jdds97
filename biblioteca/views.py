"""
Este módulo contiene las vistas de la aplicación biblioteca.
"""
from typing import Any
from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from .models import Libro, Autor, Prestamo


# pylint: disable=no-member
class CrearLibro(CreateView):
    """
    Vista para crear un nuevo libro.
    """

    model = Libro
    fields = "__all__"
    success_url = reverse_lazy("listar")


class ListarLibros(ListView):
    """
    Vista para listar todos los libros.
    """

    model = Libro

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["librosDisponibles"] = Libro.objects.filter(disponibilidad="D")
        context["librosReservados"] = Libro.objects.filter(disponibilidad="R")
        return context


class EditarLibro(UpdateView):
    """
    Vista para editar un libro existente.
    """

    model = Libro
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("listar")


class EliminarLibro(DeleteView):
    """
    Vista para eliminar un libro existente.
    """

    model = Libro
    success_url = reverse_lazy("listar")


class DetallesLibro(DetailView):
    """
    Vista para ver los detalles de un libro.
    """

    model = Libro


class CrearAutor(CreateView):
    """
    Vista para crear un nuevo autor.
    """

    model = Autor
    fields = "__all__"
    success_url = reverse_lazy("listar_autores")


class LibrosDisponibles(ListView):
    """
    Vista para listar los libros disponibles.
    """

    model = Libro
    queryset = Libro.objects.filter(disponibilidad="D")
    template_name_suffix = "_disponibles"


class MisLibros(ListView):
    """
    Vista para listar los libros prestados y devueltos por el usuario actual.
    """

    model = Prestamo
    template_name_suffix = "_mios"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["librosDevueltos"] = Prestamo.objects.filter(
            usuario=self.request.user, estado="D"
        )
        context["librosPrestados"] = Prestamo.objects.filter(
            usuario=self.request.user, estado="P"
        )
        return context


class CrearPrestamo(CreateView):
    """
    Vista para crear un nuevo préstamo de libro.
    """

    model = Prestamo
    fields = ["estado"]

    def form_valid(self, form):
        libro = get_object_or_404(Libro, pk=self.kwargs["pk"])
        usuario = self.request.user

        prestamo_existente = Prestamo.objects.filter(
            libro=libro, usuario=usuario
        ).exists()

        if not prestamo_existente:
            prestamo = form.save()
            prestamo.libro = libro
            prestamo.usuario = usuario
            prestamo.estado = "P"
            prestamo.fecha_prestamo = datetime.now()

            prestamo.save()

            libro.disponibilidad = "P"
            libro.save()

            return super().form_valid(form)

        return redirect("detalles", pk=libro.pk)


class DevolverLibro(UpdateView):
    """
    Vista para devolver un libro prestado.
    """

    model = Prestamo
    fields = ["estado"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("mis_libros")

    def form_valid(self, form):
        prestamo = form.save()
        prestamo.estado = "D"
        prestamo.save()
        libro = prestamo.libro
        libro.disponibilidad = "D"
        libro.save()
        return redirect("mis_libros", self.request.user)


class BuscarLibro(ListView):
    """
    Vista para buscar libros por título.
    """

    model = Libro
    template_name = "biblioteca/libro_buscar.html"

    def get(self, request, *args, **kwargs):
        titulo = request.GET.get("titulo")
        libros = Libro.objects.filter(titulo__icontains=titulo)
        context = {"libros": libros, "titulo": titulo}
        return render(request, self.template_name, context)
