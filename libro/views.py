from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from libro.models import *
from libro.forms import *

PAGINATE_VALUE = 25

def pagina_principal(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("lista_de_libros_faceta_lector"))
    else:
        return render(request, "libro/main.html")    

## Listas
class ListaLibrosLector(LoginRequiredMixin,ListView):
    model = Libro
    template_name = "libro/listaLibrosLector.html"
    paginate_by = PAGINATE_VALUE
    
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
            queryset = queryset.filter(autor__id=autor)
        if genero:
            queryset = queryset.filter(genero=genero)
        if relacion_lector:
            queryset = queryset.filter(lector_libro__relacion=relacion_lector)
        queryset.order_by('inicio_publicacion')
        return queryset
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["opciones"] = Lector_Libro.CHOICES_RELACION
        contexto["relaciones"] = Lector_Libro.objects.filter(lector=self.request.user)
        contexto["generos"] = Genero.objects.all().order_by('nombre')
        contexto["autores"] = Usuario.objects.exclude(libro__isnull=True).order_by('username')
        return contexto

class ListaLibrosAutor(LoginRequiredMixin,ListView):
    model = Libro
    template_name = "libro/listaLibrosAutor.html"
    paginate_by = PAGINATE_VALUE
    
    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get("estado")
        queryset = queryset.filter(autor=self.request.user)
        if estado == "p":
            queryset = queryset.filter(fin_publicacion__isnull=True)
        elif estado == "f":
            queryset = queryset.exclude(fin_publicacion__isnull=True)
        queryset.order_by('inicio_publicacion')
        return queryset

class BuscarLibros(LoginRequiredMixin,ListView):
    model = Libro
    template_name = "libro/listaLibros.html"
    paginate_by = PAGINATE_VALUE
    
    def get_queryset(self):
        queryset = super().get_queryset()
        titulo = self.request.GET.get("titulo")
        autor = self.request.GET.get("autor")
        genero = self.request.GET.get("genero")
        queryset = queryset.exclude(autor=self.request.user)
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if autor:
            queryset = queryset.filter(autor__id=autor)
        if genero:
            queryset = queryset.filter(genero=genero)
        queryset.order_by('inicio_publicacion')
        return queryset
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["generos"] = Genero.objects.all().order_by('nombre')
        contexto["autores"] = Usuario.objects.exclude(libro__isnull=True).exclude(id=self.request.user.id).order_by('username')
        contexto["libros_lector"] = Libro.objects.filter(lector__id=self.request.user.id)
        return contexto
    
class ListaAutores(LoginRequiredMixin,ListView):
    model = Usuario
    template_name = "libro/listaAutores.html"
    
    def get_queryset(self):
        busqueda = self.request.GET.get("nombre", default="")
        return Usuario.objects.filter(username__icontains=busqueda).exclude(libro__isnull=True).order_by('username')
    
## Libros
class DetallesLibro(LoginRequiredMixin,DetailView):
    model = Libro
    template_name = "libro/libro.html"
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["capitulos"] = Capitulo.objects.filter(libro=self.kwargs['pk']).order_by('numero')
        contexto["capitulos_leidos"] = Capitulo.objects.filter(libro=self.kwargs['pk'], lectores=self.request.user.id)
        contexto["lectores"] = Usuario.objects.filter(lector_libro=self.kwargs['pk'])
        contexto["opciones"] = Lector_Libro.CHOICES_RELACION
        try:
            contexto["capitulo_seleccionado"] = contexto["capitulos"].get(pk=self.kwargs['capk'])
        except:
            contexto["capitulo_seleccionado"] = None
        else:
            aux = Capitulo.objects.filter(conexiones=self.kwargs['pk']).order_by('fecha_publicacion')
            contexto["precuelas"] = aux.filter(numero__lt=contexto["capitulo_seleccionado"].numero)
            contexto["secuelas"] = aux.filter(numero__gt=contexto["capitulo_seleccionado"].numero)
        try:
            contexto["rel_lector"] = Lector_Libro.objects.filter(lector=self.request.user).filter(libro=self.kwargs['pk']).get()
        except:
            contexto["rel_lector"] = None
        return contexto

@login_required
def seguir_libro(request, pk, pg):
    lector = Usuario.objects.get(id=request.user.id)
    libro = Libro.objects.get(pk=pk)
    if lector.libros.filter(pk=pk).exists():
        lector.libros.remove(libro)
    else:
        lector.libros.add(libro)
    if pg == 1:
        return HttpResponseRedirect(reverse('busqueda_de_libros'))
    else:
        return HttpResponseRedirect(reverse('libro', kwargs={'pk':pk}))
    
class CrearLibro(LoginRequiredMixin,CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro/nuevoLibro.html"
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
class EditarLibro(LoginRequiredMixin,UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro/editarLibro.html"

@login_required
def fin_publicacion(request, pk):
    libro = Libro.objects.get(pk=pk)
    hoy = timezone.localtime(timezone.now())
    libro.fin_publicacion = hoy.date()
    libro.save()
    return HttpResponseRedirect(reverse('libro', kwargs={'pk':pk}))

class EliminarLibro(LoginRequiredMixin,DeleteView):
    model = Libro
    template_name = "libro/eliminarLibro.html"
    success_url = reverse_lazy("pagina_de_inicio")

## Capitulos
class CrearCapitulo(LoginRequiredMixin,CreateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "libro/nuevoCapitulo.html"
    
    def get_success_url(self):
        return reverse('libro', kwargs={'pk':self.object.libro.pk, 'capk':self.object.pk})
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.libro = get_object_or_404(Libro, pk=self.kwargs['libro'])
        for lector in form.instance.libro.lector.all():
            relacion = Lector_Libro.objects.get(lector=lector, libro=form.instance.libro)
            if relacion.relacion == "F":
                relacion.relacion = "L"
                relacion.save()
        return super().form_valid(form)
    
    #Propuesta de Jose Ignacio para filtrar los capitulos por el libro al que pertenecen
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['libro'] = self.kwargs['libro']
        return kwargs
    
class EditarCapitulo(LoginRequiredMixin,UpdateView):
    model = Capitulo
    form_class = CapituloForm
    template_name = "libro/editarCapitulo.html"
    
    def get_success_url(self):
        return reverse('libro', kwargs={'pk':self.object.libro.pk, 'capk':self.object.pk})

    #Propuesta de Jose Ignacio para filtrar los capitulos por el libro al que pertenecen, modificada para encajar en esta vista
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.object.pk
        kwargs['libro'] = self.object.libro.pk
        return kwargs

class EliminarCapitulo(LoginRequiredMixin,DeleteView):
    model = Capitulo
    template_name = "libro/eliminarCapitulo.html"
    def get_success_url(self):
        return reverse('libro', kwargs={'pk':self.object.libro.pk, 'capk':self.object.pk})

@login_required
def finalizar_lectura(request, pk, capk, aux):
    lector = Usuario.objects.get(id=request.user.id)
    capitulo = Capitulo.objects.get(pk=aux)
    capitulo.lectores.add(lector)
    libro = Libro.objects.get(pk=pk)
    relacion = Lector_Libro.objects.get(lector=lector, libro=libro)
    if relacion.relacion == "P":
        relacion.relacion = "L"
        relacion.save()
    elif libro.capitulo_set.filter(lectores=lector).count() == libro.capitulo_set.count():
        relacion.relacion = "F"
        relacion.save()
    return HttpResponseRedirect(reverse('libro', kwargs={'pk':pk, 'capk':capk}))

## Usuarios
class CrearUsuario(CreateView):
    model = Usuario
    form_class = NuevoUsuarioForm
    template_name = "registration/nuevoUsuario.html"
    success_url = reverse_lazy("pagina_de_inicio")
    
class EditarUsuario(LoginRequiredMixin,UpdateView):
    model = Usuario
    form_class = EditarUsuarioForm
    template_name = "registration/editarUsuario.html"

class DesactivarUsuario(LoginRequiredMixin,UpdateView):
    model = Usuario
    template_name = "registration/eliminarUsuario.html"
    fields = ['is_active']
    success_url = reverse_lazy("pagina_de_inicio")
    
class DetallesUsuario(LoginRequiredMixin,DetailView):
    model = Usuario
    template_name = "libro/usuario.html"
