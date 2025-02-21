from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from libro.models import *
from libro.forms import *

class pagina_principal(TemplateView):
    template_name = "libro/main.html"

## Listas
class lista_libros_lector(LoginRequiredMixin,ListView):
    model = Libro
    template_name = "libro/listaLibrosLector.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        usuario = Usuario.objects.get(id=self.request.user.id).pk
        titulo = self.request.GET.get("titulo")
        autor = self.request.GET.get("autor")
        genero = self.request.GET.get("genero")
        relacion_lector = self.request.GET.get("relacion")
        queryset = queryset.filter(lector__id=usuario)
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if autor:
            queryset = queryset.filter(autor_libro__username__icontains=autor)
        if genero:
            queryset = queryset.filter(genero=genero)
        if relacion_lector:
            queryset = queryset.filter(lectores_libro__relacion=relacion_lector)
        queryset.order_by('inicio_publicacion')
        return queryset
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["opciones"] = Lector_Libro.CHOICES_RELACION
        contexto["generos"] = Libro.CHOICES_GENERO
        contexto["autores"] = Usuario.objects.exclude(libro__isnull=True).order_by('username')
        return contexto

class lista_libros_autor(LoginRequiredMixin,ListView):
    model = Libro
    template_name = "libro/listaLibrosAutor.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get("estado")
        if estado == "p":
            queryset = queryset.filter(fin_publicacion__isnull=True)
        elif estado == "f":
            queryset = queryset.exclude(fin_publicacion__isnull=True)
        queryset.order_by('inicio_publicacion')
        return queryset

class buscar_libros(LoginRequiredMixin,ListView):
    model = Libro
    template_name = "libro/listaLibros.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        titulo = self.request.GET.get("titulo")
        autor = self.request.GET.get("autor")
        genero = self.request.GET.get("genero")
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if autor:
            queryset = queryset.filter(autor__username__icontains=autor)
        if genero:
            queryset = queryset.filter(genero=genero)
        queryset.order_by('inicio_publicacion')
        return queryset
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["generos"] = Libro.CHOICES_GENERO
        contexto["autores"] = Usuario.objects.exclude(libro__isnull=True).order_by('username')
        return contexto
    
class lista_autores(ListView):
    model = Usuario
    template_name = "libro/listaAutores.html"
    
    def get_queryset(self):
        busqueda = self.request.GET.get("nombre", default="")
        return Usuario.objects.filter(username__icontains=busqueda).exclude(libro__isnull=True).order_by('username')
    
## Libros
class detalles_libro(DetailView):
    model = Libro
    template_name = "libro/libro.html"
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["capitulos"] = Capitulo.objects.filter(libro=self.kwargs['pk']).order_by('numero')
        contexto["capitulos_leidos"] = Capitulo.objects.filter(libro=self.kwargs['pk'], lectores=self.request.user.id)
        contexto["lectores"] = Usuario.objects.filter(lectores_libro=self.kwargs['pk'])
        return contexto
    
def leyendo_libro(request, pk):
    lector = Usuario.objects.get(id=request.user.id)
    libro = Libro.objects.get(pk=pk)
    libro.lectores.add(lector)
    return HttpResponseRedirect(reverse('libro', kwargs={'pk':pk}))
    
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

## Capitulos
class crear_capitulo(LoginRequiredMixin,CreateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "libro/nuevoCapitulo.html"
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.libro = get_object_or_404(Libro, pk=self.kwargs['libro'])
        return super().form_valid(form)
    
    #Propuesta de Jose Ignacio para filtrar los capitulos por el libro al que pertenecen
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['libro'] = self.kwargs['libro']
        return kwargs
    
class editar_capitulo(LoginRequiredMixin,UpdateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "libro/editarCapitulo.html"

    #Propuesta de Jose Ignacio para filtrar los capitulos por el libro al que pertenecen, modificada para encajar en esta vista
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.object.pk
        kwargs['libro'] = self.object.libro.pk
        return kwargs

class eliminar_capitulo(LoginRequiredMixin,DeleteView):
    model = Capitulo
    template_name = "libro/eliminarCapitulo.html"
    success_url = reverse_lazy("pagina_de_inicio")
    
class leer_capitulo(DetailView):
    model = Capitulo
    template_name = "libro/capitulo.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        aux = Capitulo.objects.filter(conexiones=self.kwargs['pk']).order_by('fecha_publicacion')
        contexto["precuelas"] = aux.filter(numero__lt=self.kwargs['numero'])
        contexto["secuelas"] = aux.filter(numero__gt=self.kwargs['numero'])
        contexto["lectores"] = Usuario.objects.filter(lectores_capitulo=self.kwargs['pk'])
        return contexto
    
def finalizar_lectura(request, pk, aux):
    lector = Usuario.objects.get(id=request.user.id)
    capitulo = Capitulo.objects.get(pk=pk)
    capitulo.lectores.add(lector)
    if aux > 0:
        secuela = Capitulo.objects.get(pk=aux)
        return HttpResponseRedirect(reverse('capitulo', kwargs={'pk':aux, 'numero':secuela.numero}))
    else:
        return HttpResponseRedirect(reverse('libro', kwargs={'pk':capitulo.libro.pk}))

## Usuarios
class crear_usuario(CreateView):
    model = Usuario
    form_class = NuevoUsuarioForm
    template_name = "registration/nuevoUsuario.html"
    
class editar_usuario(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = EditarUsuarioForm
    template_name = "registration/editarUsuario.html"

# Preguntar la forma de desactivar un usuario
class desactivar_usuario(LoginRequiredMixin,DeleteView):
    model = Usuario
    template_name = "registration/eliminarUsuario.html"
    success_url = reverse_lazy("pagina_de_inicio")
    
class detalles_usuario(DetailView):
    model = Usuario
    template_name = "libro/usuario.html"
    
    def get_context_data(self, **kwargs):
        libros = super().get_context_data(**kwargs)
        libros["libros_autor"] = Libro.objects.filter(autor=self.kwargs['pk']).order_by('inicio_publicacion')
        libros["libros_lector"] = Libro.objects.filter(lectores=self.kwargs['pk']).order_by('inicio_publicacion')
        return libros
