from django.urls import path
from .views import pagina_principal, lista_libros, detalles_libro, lista_autores, detalles_autor, detalles_lector, leer_capitulo, crear_libro, editar_libro, eliminar_libro, crear_capitulo, editar_capitulo, eliminar_capitulo, crear_autor, editar_autor, eliminar_autor, crear_lector, editar_lector, eliminar_lector

urlpatterns = [
    path("", pagina_principal.as_view(), name="pagina_de_inicio"),
    path("libros/", lista_libros.as_view(), name="lista_de_libros"),
    path("libro/<int:pk>", detalles_libro.as_view(), name="libro"),
    path("autores/", lista_autores.as_view(), name="lista_de_autores"),
    path("autor/<int:pk>", detalles_autor.as_view(), name="autor"),
    path("lector/", detalles_lector.as_view(), name="lector"),
    path("capitulo/<int:pk>", leer_capitulo.as_view(), name="capitulo"),
    ##CRUDS
    path("libro/nuevo/", crear_libro.as_view(), name="nuevo_libro"),
    path("libro/editar/<int:pk>", editar_libro.as_view(), name="editar_el_libro"),
    path("libro/eliminar/<int:pk>", eliminar_libro.as_view(), name="eliminar_el_libro"),
    path("capitulo/nuevo/<int:libro>", crear_capitulo.as_view(), name="nuevo_capitulo"),
    path("capitulo/editar/<int:pk>", editar_capitulo.as_view(), name="editar_el_capitulo"),
    path("capitulo/eliminar/<int:pk>", eliminar_capitulo.as_view(), name="eliminar_el_capitulo"),
    path("autor/nuevo/", crear_autor.as_view(), name="nuevo_autor"),
    path("autor/editar/<int:pk>", editar_autor.as_view(), name="editar_el_autor"),
    path("autor/eliminar/<int:pk>", eliminar_autor.as_view(), name="eliminar_el_autor"),
    path("lector/nuevo/", crear_lector.as_view(), name="nuevo_lector"),
    path("lector/editar/<int:pk>", editar_lector.as_view(), name="editar_el_lector"),
    path("lector/eliminar/<int:pk>", eliminar_lector.as_view(), name="eliminar_el_lector"),
]