from django.urls import path
from .views import pagina_principal, lista_libros, detalles_libro, crear_libro, editar_libro, eliminar_libro, crear_capitulo, editar_capitulo, eliminar_capitulo, lista_autores, detalles_autor, detalles_lector, leer_capitulo

urlpatterns = [
    path("", pagina_principal.as_view(), name="pagina_de_inicio"),
    path("libros/", lista_libros.as_view(), name="lista_de_libros"),
    path("libro/<int:pk>", detalles_libro.as_view(), name="libro"),
    path("libro/nuevo", crear_libro.as_view(), name="nuevo_libro"),
    path("libro/editar/<int:pk>", editar_libro.as_view(), name="editar_el_libro"),
    path("libro/eliminar/<int:pk>", eliminar_libro.as_view(), name="eliminar_el_libro"),
    path("capitulo/nuevo/<int:pk>", crear_capitulo.as_view(), name="nuevo_capitulo"),
    path("capitulo/editar/<int:pk>", editar_capitulo.as_view(), name="editar_el_capitulo"),
    path("capitulo/eliminar/<int:pk>", eliminar_capitulo.as_view(), name="eliminar_el_capitulo"),
    path("autores/", lista_autores.as_view(), name="lista_de_autores"),
    path("autor/<int:pk>", detalles_autor.as_view(), name="autor"),
    path("capitulo/<int:pk>", leer_capitulo.as_view(), name="capitulo"),
]