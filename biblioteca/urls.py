from django.urls import path
from .views import Crear_libro,Listar_libros,Editar_libro,Eliminar_libro,Detalles_libro
from.views import Crear_autor


urlpatterns = [
    path('libro/new/',Crear_libro.as_view(),name='crear'),
    path('',Listar_libros.as_view(),name='listar'),
    path('libro/editar/<int:pk>/',Editar_libro.as_view(),name='editar'),
    path('libro/eliminar/<int:pk>/',Eliminar_libro.as_view(),name='borrar'),
    path('libro/detalles/<int:pk>/',Detalles_libro.as_view(),name='detalles'),
    path('autor/new/',Crear_autor.as_view(),name='detalles'),
]



