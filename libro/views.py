from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from libro.models import Usuario, Autor, Lector, Libro, Capitulo
from libro.forms import NuevoLibroForm, EditarLibroForm, CapituloForm, NuevoUsuarioForm, EditarUsuarioForm, AutorFormset

class pagina_principal(TemplateView):
    template_name = "libro/main.html"
    
class nuevo_usuario(TemplateView):
    template_name = "libro/nuevoUsuario.html"

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
    template_name = "libro/nuevoCapitulo.html"
    
    def form_valid(self, form):
        form.instance.autor = self.request.user     
        form.instance.libro = get_object_or_404(Libro, pk=self.kwargs['pk'])
        return super().form_valid(form)
    
class editar_capitulo(LoginRequiredMixin,UpdateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "libro/editarCapitulo.html"
    
class eliminar_capitulo(LoginRequiredMixin,DeleteView):
    model = Capitulo
    template_name = "libro/eliminarCapitulo.html"
    success_url = reverse_lazy("libro")
    
class crear_autor(CreateView):
    model = Usuario
    form_class = NuevoUsuarioForm
    template_name = "libro/nuevoAutor.html"
    
    def get_context_data(self, **kwargs):
        data = super(crear_autor, self).get_context_data(**kwargs)
        if self.request.POST:
            data['FormAutor'] = AutorFormset(self.request.POST)
        else:
            data['FormAutor'] = AutorFormset()
        return data
    
    def form_valid(self, form):
        form.instance.es_autor = True
        context = self.get_context_data(form=form)
        formset = context['FormAutor']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)
    
class editar_autor(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = EditarUsuarioForm
    template_name = "libro/editarAutor.html"
    
    def get_context_data(self, **kwargs):
        data = super(crear_autor, self).get_context_data(**kwargs)
        if self.request.POST:
            data['FormAutor'] = AutorFormset(self.request.POST, instance=self.object)
            data['FormAutor'].full_clean()
        else:
            data['FormAutor'] = AutorFormset()
        return data
    
    def form_valid(self, form):
        form.instance.es_autor = True
        context = self.get_context_data(form=form)
        formset = context['FormAutor']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)
    
class eliminar_autor(LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name = "libro/eliminarAutor.html"
    success_url = reverse_lazy("pagina_de_inicio")
    
class crear_lector(CreateView):
    model = Usuario
    form_class = NuevoUsuarioForm
    template_name = "libro/nuevoLector.html"
    
    def form_valid(self, form):
        form.instance.es_lector = True
        return super().form_valid(form)
    
class editar_lector(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = EditarUsuarioForm
    template_name = "libro/editarLector.html"
    
class eliminar_lector(LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name = "libro/eliminarLector.html"
    success_url = reverse_lazy("pagina_de_inicio")
    
class lista_autores(ListView):
    model = Autor
    template_name = "libro/listaAutores.html"
    
    def get_queryset(self):
        return Autor.objects.all().order_by('usuario')
    
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
    
    def get_context_data(self, **kwargs):
        libros = super().get_context_data(**kwargs)
        libros["libros"] = Libro.objects.filter(lectores=self.kwargs['pk']).order_by('inicio_publicacion')
        return libros
    
class leer_capitulo(DetailView):
    model = Capitulo
    template_name = "libro/capitulo.html"

    def get_context_data(self, **kwargs):
        capitulos = super().get_context_data(**kwargs)
        capitulos["precuelas"] = Capitulo.objects.filter(secuela_de=self.kwargs['pk']).order_by('inicio_publicacion')
        capitulos["secuelas"] = Capitulo.objects.filter(capitulos=self.kwargs['pk']).order_by('inicio_publicacion')
        return capitulos