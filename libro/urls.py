from django.urls import path
from .views import *

urlpatterns = [
    path("", pagina_principal.as_view(), name="pagina_de_inicio"),
    path("libros_lector/", lista_libros_lector.as_view(), name="lista_de_libros_faceta_lector"),
    path("libros_autor/", lista_libros_autor.as_view(), name="lista_de_libros_faceta_autor"),
    path("libros_busqueda/", buscar_libros.as_view(), name="busqueda_de_libros"),
    path("libro/<int:pk>", detalles_libro.as_view(), name="libro"),
    path("autores/", lista_autores.as_view(), name="lista_de_autores"),
    path("usuario/<int:pk>", detalles_usuario.as_view(), name="usuario"),
    path("capitulo/<int:pk>/<int:numero>", leer_capitulo.as_view(), name="capitulo"),
    path("libro/<int:pk>/leyendo", leyendo_libro, name="leyendo"),
    path("capitulo_leido/<int:pk>/<int:aux>", finalizar_lectura, name="capitulo_leido"),
    path("libro/<int:pk>/fin_publicacion", fin_publicacion, name="fin_de_publicacion"),
    ##CRUDS
    path("libro/nuevo/", crear_libro.as_view(), name="nuevo_libro"),
    path("libro/editar/<int:pk>", editar_libro.as_view(), name="editar_el_libro"),
    path("libro/eliminar/<int:pk>", eliminar_libro.as_view(), name="eliminar_el_libro"),
    path("capitulo/nuevo/<int:libro>", crear_capitulo.as_view(), name="nuevo_capitulo"),
    path("capitulo/editar/<int:pk>", editar_capitulo.as_view(), name="editar_el_capitulo"),
    path("capitulo/eliminar/<int:pk>", eliminar_capitulo.as_view(), name="eliminar_el_capitulo"),
    path("usuario/nuevo/", crear_usuario.as_view(), name="nuevo_usuario"),
    path("usuario/editar/<int:pk>", editar_usuario.as_view(), name="editar_el_usuario"),
    path("usuario/desactivar/<int:pk>", desactivar_usuario.as_view(), name="desactivar_el_usuario"),
]