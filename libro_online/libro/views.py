from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from libro.models import Autor, Lector, Libro, Capitulo, Seccion

class main_page(TemplateView):
    template_name = ""

class lista_libros(ListView):
    model = Libro
    template_name = ""
    
class detalles_libro(DetailView):
    model = Libro
    template_name = ""
    
    def get_context_data(self, **kwargs):
        capitulos = super().get_context_data(**kwargs)
        capitulos["secciones"] = Seccion.objects.filter(libro = self.kwargs['pk']).order_by('numero')
        if capitulos["secciones"].count <= 1:
            capitulos["capitulos"] = Capitulo.objects.filter(seccion = capitulos["secciones"][0]['pk']).order_by('numero')
        else:
            for i in capitulos["secciones"]:
                capitulos["secciones"][i]["capitulos"] = Capitulo.objects.filter(seccion = capitulos["secciones"][i]['pk']).order_by('numero')
        return capitulos