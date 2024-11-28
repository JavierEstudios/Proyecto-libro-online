from django.urls import path
from .views import pagina_principal, lista_libros, detalles_libro, lista_autores, detalles_autor, detalles_lector, leer_capitulo

urlpatterns = [
    path("", pagina_principal.as_view(), name="pagina_de_inicio"),
    path("libros/", lista_libros.as_view(), name="lista_de_libros"),
    path("libro/<int:pk>", detalles_libro.as_view(), name="libro"),
    path("autores/", lista_autores.as_view(), name="lista_de_autores"),
    path("autor/<int:pk>", detalles_autor.as_view(), name="autor"),
    path("capitulo/<int:pk>", leer_capitulo.as_view(), name="capitulo"),
]