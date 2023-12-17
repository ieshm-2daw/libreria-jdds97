"""
Este módulo contiene las vistas de la aplicación biblioteca.
"""
from typing import Any
from datetime import datetime, timedelta
from urllib import request
from django.db.models import Case, Value, When, Max, Avg
from django.http import  HttpResponse
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
from .models import Libro, Autor, Prestamo, Genero


# pylint: disable=no-member
class CrearLibro(CreateView):
    """
    Vista para crear un nuevo libro.
    """

    model = Libro
    fields = "__all__"
    success_url = reverse_lazy("listar")


# Editar el martes 1
class Bibliotecario(ListView):
    """
    Vista para listar todos los libros.
    """

    model = Prestamo
    queryset = Libro.objects.filter(disponibilidad="D")
    template_name_suffix = "_bibliotecario"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # type: ignore
        if self.request.user == "bibliotecario":
            context = super().get_context_data(**kwargs)
            context["numeroPrestamos"] = Prestamo.objects.count()
            context["numeroDisponibles"] = Libro.objects.filter(
                disponibilidad="D"
            ).count()
            print(context["numeroDisponibles"])
            context["librosNoDevueltos"] = Prestamo.objects.filter(
                fecha_devolucion__lt=datetime.now()
            )
            context["librosAdevolver"] = Prestamo.objects.filter(
                fecha__devolucion__gt=datetime.now() - timedelta(days=7)
            )
            context["topLibros"] = Libro.objects.filter(valoracion__gte=4)
            context["librosDisponibles"] = Libro.objects.filter(disponibilidad="D")
            context["librosReservados"] = Libro.objects.filter(disponibilidad="R")
            return context


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


class CrearPrestamo(View):
    """
    Vista para crear un nuevo préstamo de libro.
    """

    def get(self, pk):
        """
        Get
        """
        libro = get_object_or_404(Libro, pk=pk, disponibilidad="D")
        return render(self.request, "biblioteca/prestamo_form.html", {"libro": libro})

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
            fecha_devolucion=None,
            usuario=usuario,
            estado="P",
        )
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

    def get(self, *args, **kwargs):
        titulo = self.request.GET.get("titulo")
        libros = Libro.objects.filter(titulo__icontains=titulo)
        context = {"libros": libros, "titulo": titulo}
        return render(self.request, self.template_name, context)


class FiltrarCategoria(ListView):
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


# Editar martes 2 lio de cosas gordas de documentacion django 
"""

class ValorarLibro(View):
    def get(self,request,pk):
        libro = get_object_or_404(Libro, pk=pk)
        prestamo=Prestamo.objects.filter(libro=libro,usuario=request.user)
        return render(self.request, "biblioteca/libro_valorar.html", {"prestamo": prestamo})
    def post(self,request,pk):
        libro = get_object_or_404(Libro, pk=pk)
        prestamo=Prestamo.objects.filter(libro=libro,usuario=request.user)
        valoracion=Valoracion.objects.create(
            libro=libro,
            usuario=request.user,
            valoracion=request.POST.get("rating"),
        )
        libro.rating=Valoracion.objects.filter(libro=libro).aggregate(Avg("valoracion"))
        libro.save()
        return redirect("detalles",libro.pk)
    model = Libro
    fields = ["rating"]
    template_name_suffix = "_valorar"
    success_url = reverse_lazy("listar")

    def form_valid(self, form):
        libro = Libro.objects.get(pk=self.kwargs["pk"])
        valoracion = libro.rating
        valoracion.libro = libro
        valoracion.usuario = self.request.user
        valoracion.valoracion = form.cleaned_data["rating"]
        valoracion.save()
        media = Libro.objects.aggregate(Avg())
        libro.rating=(Avg(libro.rating))
        libro.rating = (libro.rating + valoracion.rating) / len.libro.rating
        libro.valoracion
        Valoracion.objects.aggregate(
            Avg("rating")
        )
        libro.save()
        return redirect("listar", self.request.user)
class ValoracionMedia(UpdateView):
    model = Prestamo
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("listar")

    def form_valid(self, form):
        libro = Libro.objects.get(pk=self.kwargs["pk"])
        valoracion = libro.rating
        valoracion.libro = libro
        valoracion.usuario = self.request.user
        valoracion.valoracion = form.cleaned_data["rating"]
        valoracion.save()
        promedio = sum([v.valoracion for v in libro.rating.all()]) / len(
            libro.rating.all()
        )
        media = Libro.objects.aggregate(Avg())
        libro.rating = (libro.rating + valoracion.rating) / 2
        libro.valoracion
        prestamo.libro = libro
        prestamo.libro.rating, prestamo.valoracion = Valoracion.objects.aggregate(
            Avg("rating")
        )
        libro.save()
        return redirect("listar", self.request.user)
"""
