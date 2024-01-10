"""
Este módulo contiene las vistas de la aplicación biblioteca.
"""
from typing import Any
from datetime import datetime, timedelta
from django.db.models import Case, Value, When, Max, Avg
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Libro, Autor, Prestamo, Genero


# pylint: disable=no-member
class CrearLibro(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo libro.
    """

    model = Libro
    fields = "__all__"
    success_url = reverse_lazy("listar")


class ListarLibros(LoginRequiredMixin, ListView):
    """
    Vista para listar todos los libros.
    """

    model = Libro
    paginate_by = 5

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["usuario"] = self.request.user.get_username()
        if context["usuario"] == "bibliotecario":
            context["numeroPrestamos"] = Prestamo.objects.count()
            context["numeroDisponibles"] = Libro.objects.filter(
                disponibilidad="D"
            ).count()
            context["librosNoDevueltos"] = Prestamo.objects.filter(
                fecha_devolucion__lt=datetime.now()
            )
            context["librosAdevolver"] = Prestamo.objects.filter(
                fecha_devolucion__gt=datetime.now() + timedelta(days=7)
            )
            context["topLibros"] = Libro.objects.filter(rating__gte=4)
        else:
            context["librosDisponibles"] = Libro.objects.filter(disponibilidad="D")
            context["librosReservados"] = Libro.objects.filter(disponibilidad="R")
        return context


class EditarLibro(LoginRequiredMixin, UpdateView):
    """
    Vista para editar un libro existente.
    """

    model = Libro
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("listar")


class EliminarLibro(LoginRequiredMixin, DeleteView):
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


class CrearAutor(LoginRequiredMixin, CreateView):
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


class MisLibros(LoginRequiredMixin, ListView):
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


# @login_required -->Para la forma de funciones
class CrearPrestamo(LoginRequiredMixin, View):
    """
    Vista para crear un nuevo préstamo de libro.
    """

    def get(self, request, pk):
        """
        Get
        """
        libro = get_object_or_404(Libro, pk=pk, disponibilidad="D")
        return render(
            request,
            "biblioteca/prestamo_form.html",
            {"libro": libro},
        )

    def post(self, pk):
        """
        Post
        """
        libro = Libro.objects.get(pk=pk)
        usuario = self.request.user
        libro.disponibilidad = "P"
        libro.save()
        Prestamo.objects.create(
            libro=libro,
            fecha_prestamo=datetime.now(),
            fecha_devolucion=datetime.now() + timedelta(days=10),
            usuario=usuario,
            estado="P",
        )
        return redirect("detalles", libro.pk)


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
    template_name_suffix = "_buscar"

    def get(self, *args, **kwargs):
        titulo = self.request.GET.get("titulo")
        libros = Libro.objects.filter(titulo__icontains=titulo)
        context = {"libros": libros, "titulo": titulo}
        return render(self.request, self.template_name, context)


class FiltrarCategoria(ListView):
    """
    Vista para filtrar libros por categoría.
    """

    model = Libro
    queryset = Libro.objects.filter(disponibilidad="D")
    template_name_suffix = "_categoria"

    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
        opciones = self.request.GET.get("opciones")
        if self.queryset is not None:
            self.queryset = self.queryset.filter(
                genero__in=Genero.objects.filter(categoria=opciones)
            )
        return super().get(*args, **kwargs)
