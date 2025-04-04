from django.urls import path
from .views import *

urlpatterns = [
    path("", pagina_principal, name="pagina_de_inicio"),
    path("lector/", ListaLibrosLector.as_view(), name="lista_de_libros_faceta_lector"),
    path("autor/", ListaLibrosAutor.as_view(), name="lista_de_libros_faceta_autor"),
    path("busqueda/", BuscarLibros.as_view(), name="busqueda_de_libros"),
    ##Libros
    path("libro/<int:pk>/<int:capk>/", DetallesLibro.as_view(), name="libro"),
    path("libro/nuevo/", CrearLibro.as_view(), name="nuevo_libro"),
    path("libro/editar/<int:pk>/", EditarLibro.as_view(), name="editar_el_libro"),
    path("libro/eliminar/<int:pk>/", EliminarLibro.as_view(), name="eliminar_el_libro"),
    path("libro/<int:pk>/leyendo/<int:pg>/", seguir_libro, name="leyendo"),
    path("libro/<int:pk>/fin_publicacion/", fin_publicacion, name="fin_de_publicacion"),
    ##Capitulos
    path("capitulo_leido/<int:pk>/<int:capk>/<int:aux>/", finalizar_lectura, name="capitulo_leido"),
    path("capitulo/nuevo/<int:libro>/", CrearCapitulo.as_view(), name="nuevo_capitulo"),
    path("capitulo/editar/<int:pk>/", EditarCapitulo.as_view(), name="editar_el_capitulo"),
    path("capitulo/eliminar/<int:pk>/", EliminarCapitulo.as_view(), name="eliminar_el_capitulo"),
    path("comprobacion/<int:pk>/", comprobar_lectura_finalizada, name="comprobacion"),
    ##Usuarios
    path("usuario/<int:pk>/", DetallesUsuario.as_view(), name="usuario"),
    path("usuario/nuevo/", CrearUsuario.as_view(), name="nuevo_usuario"),
    path("usuario/editar/<int:pk>/", EditarUsuario.as_view(), name="editar_el_usuario"),
    path("usuario/desactivar/<int:pk>/", DesactivarUsuario.as_view(), name="desactivar_el_usuario"),
]