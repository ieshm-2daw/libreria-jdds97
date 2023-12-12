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
from django.urls import reverse_lazy
from .models import Libro, Autor, Prestamo, Usuario
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


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
    template_name_suffix = "_update_form"


class Eliminar_libro(DeleteView):
    model = Libro
    success_url = reverse_lazy("listar")


class Detalles_libro(DetailView):
    model = Libro


class Crear_autor(CreateView):
    model = Autor
    fields = "__all__"
    success_url = reverse_lazy("listar_autores")


"""
class Crear_prestamo(View):
    template_name = "biblioteca/prestamo_form.html"
    libro = None

    def get(self, request, pk):
        self.libro = get_object_or_404(Libro, pk=pk)
        return render(request, self.template_name, {"libro": self.libro})

    def post(self, request, pk):
        libro = Libro.objects.get(pk=pk)
        Prestamo.objects.create(
            usuario=request.user,
            libro=self.libro,
            fecha_prestamo="1997-12-12",
            estado="P",
        )
        self.libro.disponibilidad = "P"
        self.libro.save()
        return redirect("detalles", self.libro.pk)


"""
"""
class Devolver_Libro(View):
    template_name = "bibilioteca/devolver_libro.html"
    libro=None
    def get(self,request, pk):
        self.libro = get_object_or_404(Libro, pk=pk)
        return render(request, self.template_name, {"libro": self.libro})
    def post(self,request, pk):
        self.libro = get_object_or_404(Libro, pk=pk)
        prestamo = Libro.objects.filter(disponibilidad="P", usuario=request.user)
        # filter libro prestadp ,el usuario y el estado prestado,recsatar
        prestamo.disponibilidad = "D"
        self.libro.disponibilidad = "D"
        return redirect("detalles",self.libro.pk)
"""


class Libros_disponibles(View):
    def get(self, request):
        libros = Libro.objects.filter(disponibilidad="D")
        return render(request, "biblioteca/libros_disponibles.html", {"libros": libros})


class Libros_reservados(View):
    def get(self, request):  # obtener el usuario logueado
        reservas = Prestamo.objects.filter(usuario=request.user).order_by(
            "fecha_creacion"
        )
        return render(
            request, "biblioteca/libros_reservados.html", {"reservas": reservas}
        )


class Crear_prestamo(CreateView):
    model = Prestamo
    fields = "__all__"
    success_url = reverse_lazy("listar")

    def form_valid(self, form):
        libro = Libro.objects.get(pk=self.kwargs["pk"])
        form.instance.usuario = self.request.user
        form.instance.libro = libro
        form.instance.estado = "P"
        libro.disponibilidad = "P"
        libro.save()
        return super().form_valid(form)


class Devolver_Libro(View):
    def delete(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        prestamo = Prestamo.objects.filter(disponibilidad="P", usuario=request.user)
        prestamo.update(disponibilidad="D")
        libro.disponibilidad = "D"
        libro.save()
        return redirect("listar")
