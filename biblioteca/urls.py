"""
URLs de la aplicación biblioteca.
"""
from django.urls import path
from .views import (
    CrearLibro,
    ListarLibros,
    EditarLibro,
    EliminarLibro,
    DetallesLibro,
    CrearPrestamo,
    DevolverLibro,
    LibrosDisponibles,
    MisLibros,
    BuscarLibro,
)
from .views import CrearAutor


urlpatterns = [
    path("libro/new/", CrearLibro.as_view(), name="crear"),
    path("", ListarLibros.as_view(), name="listar"),
    path("libro/editar/<int:pk>/", EditarLibro.as_view(), name="editar"),
    path("libro/eliminar/<int:pk>/", EliminarLibro.as_view(), name="borrar"),
    path("libro/detalles/<int:pk>/", DetallesLibro.as_view(), name="detalles"),
    path("autor/new/", CrearAutor.as_view(), name="crear_autor"),
    path(
        "prestamo/new/<str:usuario>/<int:pk>/",
        CrearPrestamo.as_view(),
        name="prestamo",
    ),
    path(
        "prestamo/devolver/<str:usuario>/<int:pk>/",
        DevolverLibro.as_view(),
        name="devolver",
    ),
    path(
        "libros_disponibles/<str:usuario>/",
        LibrosDisponibles.as_view(),
        name="libros_disponibles",
    ),
    path("mis_libros/<str:usuario>/", MisLibros.as_view(), name="mis_libros"),
    path("buscar/", BuscarLibro.as_view(), name="buscar"),
]
