from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from libro.models import Usuario, Libro, Capitulo
from libro.forms import LibroForm, CapituloForm, NuevoUsuarioForm, EditarUsuarioForm

class pagina_principal(TemplateView):
    template_name = "libro/main.html"

class lista_libros(ListView):
    model = Libro
    template_name = "libro/listaLibros.html"
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Libro.objects.filter().order_by('inicio_publicacion')
    
class detalles_libro(DetailView):
    model = Libro
    template_name = "libro/libro.html"
    
    def get_context_data(self, **kwargs):
        capitulos = super().get_context_data(**kwargs)
        capitulos["capitulos"] = Capitulo.objects.filter(libro=self.kwargs['pk']).order_by('numero')
        return capitulos
    
class crear_libro(LoginRequiredMixin,CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro/nuevoLibro.html"
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
class editar_libro(LoginRequiredMixin,UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro/editarLibro.html"
    
def fin_publicacion(request, pk):
    libro = Libro.objects.get(pk=pk)
    hoy = timezone.localtime(timezone.now())
    libro.fin_publicacion = hoy.date()
    libro.save()
    return HttpResponseRedirect(reverse('libro', kwargs={'pk':pk}))

class eliminar_libro(LoginRequiredMixin,DeleteView):
    model = Libro
    template_name = "libro/eliminarLibro.html"
    success_url = reverse_lazy("pagina_de_inicio")

class crear_capitulo(LoginRequiredMixin,CreateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "libro/nuevoCapitulo.html"
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.libro = get_object_or_404(Libro, pk=self.kwargs['libro'])
        return super().form_valid(form)
    
class editar_capitulo(LoginRequiredMixin,UpdateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "libro/editarCapitulo.html"

class eliminar_capitulo(LoginRequiredMixin,DeleteView):
    model = Capitulo
    template_name = "libro/eliminarCapitulo.html"
    success_url = reverse_lazy("pagina_de_inicio")
    
class crear_usuario(CreateView):
    model = Usuario
    form_class = NuevoUsuarioForm
    template_name = "registration/nuevoUsuario.html"
    
class editar_usuario(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = EditarUsuarioForm
    template_name = "registration/editarUsuario.html"
    
class eliminar_usuario(LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name = "registration/eliminarUsuario.html"
    success_url = reverse_lazy("pagina_de_inicio")
    
class lista_autores(ListView):
    model = Usuario
    template_name = "libro/listaAutores.html"
    
    def get_queryset(self):
        return Usuario.objects.filter().order_by('username') ##TODO: Filtrar por usuarios con libros
    
class detalles_usuario(DetailView):
    model = Usuario
    template_name = "libro/usuario.html"
    
    def get_context_data(self, **kwargs):
        libros = super().get_context_data(**kwargs)
        libros["libros"] = Libro.objects.filter(autor=self.kwargs['pk']).order_by('inicio_publicacion')
        return libros
    
class leer_capitulo(DetailView):
    model = Capitulo
    template_name = "libro/capitulo.html"

    def get_context_data(self, **kwargs):
        capitulos = super().get_context_data(**kwargs)
        capitulos["secuela_de"] = Capitulo.objects.filter(secuela_de=self.kwargs['pk']).order_by('fecha_publicacion')
        return capitulos