from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from libro.models import Autor, Lector, Libro, Capitulo
from libro.forms import NuevoLibroForm, EditarLibroForm, CapituloForm, NuevoAutorForm, EditarAutorForm, NuevoLectorForm, EditarLectorForm

class pagina_principal(TemplateView):
    template_name = "libro/main.html"

class lista_libros(ListView):
    model = Libro
    template_name = "libro/listaLibros.html"
    
    def get_queryset(self):
        return Libro.objects.all().order_by('inicio_publicacion')
    
class detalles_libro(DetailView):
    model = Libro
    template_name = "libro/libro.html"
    
    def get_context_data(self, **kwargs):
        capitulos = super().get_context_data(**kwargs)
        capitulos["capitulos"] = Capitulo.objects.filter(libro=self.kwargs['pk']).order_by('numero')
        return capitulos
    
class crear_libro(LoginRequiredMixin,CreateView):
    model = Libro
    form_class = NuevoLibroForm
    template_name = "libro/nuevoLibro.html"
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
class editar_libro(LoginRequiredMixin,UpdateView):
    model = Libro
    form_class = EditarLibroForm
    template_name = "libro/editarLibro.html"
    
class eliminar_libro(LoginRequiredMixin,DeleteView):
    model = Libro
    template_name = "libro/eliminarLibro.html"
    success_url = reverse_lazy("autor")
    
class crear_capitulo(LoginRequiredMixin,CreateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "capitulo/nuevoCapitulo.html"
    
    def form_valid(self, form):
        form.instance.autor = self.request.user     
        form.instance.libro = get_object_or_404(Libro, pk=self.kwargs['pk'])
        return super().form_valid(form)
    
class editar_capitulo(LoginRequiredMixin,UpdateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "capitulo/editarCapitulo.html"
    
class eliminar_capitulo(LoginRequiredMixin,DeleteView):
    model = Capitulo
    template_name = "capitulo/eliminarCapitulo.html"
    success_url = reverse_lazy("libro")
    
class crear_autor(CreateView):
    model = Autor
    form_class = NuevoAutorForm
    template_name = "autor/nuevoAutor.html"
    
class editar_autor(LoginRequiredMixin,UpdateView):
    model = Autor
    form_class = EditarAutorForm
    template_name = "autor/editarAutor.html"
    
class eliminar_autor(LoginRequiredMixin,DeleteView):
    model = Autor
    template_name = "autor/eliminarAutor.html"
    
class crear_lector(CreateView):
    model = Lector
    form_class = NuevoLectorForm
    template_name = "lector/nuevoLector.html"
    
class editar_lector(LoginRequiredMixin,UpdateView):
    model = Lector
    form_class = EditarLectorForm
    template_name = "lector/editarLector.html"
    
class eliminar_lector(LoginRequiredMixin,DeleteView):
    model = Lector
    template_name = "lector/eliminarLector.html"
    
class lista_autores(ListView):
    model = Autor
    template_name = "libro/listaAutores.html"
    
    def get_queryset(self):
        return Autor.objects.all().order_by('username')
    
class detalles_autor(DetailView):
    model = Autor
    template_name = "libro/autor.html"
    
    def get_context_data(self, **kwargs):
        libros = super().get_context_data(**kwargs)
        libros["libros"] = Libro.objects.filter(autores=self.kwargs['pk']).order_by('inicio_publicacion')
        return libros
    
class detalles_lector(LoginRequiredMixin,DetailView):
    model = Lector
    template_name = ""
    
class leer_capitulo(DetailView):
    model = Capitulo
    template_name = "libro/capitulo.html"

    def get_context_data(self, **kwargs):
        capitulos = super().get_context_data(**kwargs)
        capitulos["precuelas"] = Capitulo.objects.filter(secuela_de=self.kwargs['pk']).order_by('inicio_publicacion')
        capitulos["secuelas"] = Capitulo.objects.filter(capitulos=self.kwargs['pk']).order_by('inicio_publicacion')
        return capitulos