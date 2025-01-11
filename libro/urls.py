from django.urls import path
from .views import fin_publicacion, pagina_principal, lista_libros, detalles_libro, lista_autores, detalles_usuario, leer_capitulo, crear_libro, editar_libro, eliminar_libro, crear_capitulo, editar_capitulo, eliminar_capitulo, crear_usuario, editar_usuario, eliminar_usuario

urlpatterns = [
    path("", pagina_principal.as_view(), name="pagina_de_inicio"),
    path("libros/", lista_libros.as_view(), name="lista_de_libros"),
    path("libro/<int:pk>", detalles_libro.as_view(), name="libro"),
    path("autores/", lista_autores.as_view(), name="lista_de_autores"),
    path("usuario/<int:pk>", detalles_usuario.as_view(), name="usuario"),
    path("capitulo/<int:pk>", leer_capitulo.as_view(), name="capitulo"),
    path("libro/fin_publicacion/<int:pk>", fin_publicacion, name="fin_de_publicacion"),
    ##CRUDS
    path("libro/nuevo/", crear_libro.as_view(), name="nuevo_libro"),
    path("libro/editar/<int:pk>", editar_libro.as_view(), name="editar_el_libro"),
    path("libro/eliminar/<int:pk>", eliminar_libro.as_view(), name="eliminar_el_libro"),
    path("capitulo/nuevo/<int:libro>", crear_capitulo.as_view(), name="nuevo_capitulo"),
    path("capitulo/editar/<int:pk>", editar_capitulo.as_view(), name="editar_el_capitulo"),
    path("capitulo/eliminar/<int:pk>", eliminar_capitulo.as_view(), name="eliminar_el_capitulo"),
    path("usuario/nuevo/", crear_usuario.as_view(), name="nuevo_usuario"),
    path("usuario/editar/<int:pk>", editar_usuario.as_view(), name="editar_el_usuario"),
    path("usuario/eliminar/<int:pk>", eliminar_usuario.as_view(), name="eliminar_el_usuario"),
]