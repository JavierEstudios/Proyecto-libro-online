from django import forms
from .models import Autor, Lector, Libro, Capitulo

class NuevoLibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo','descripcion','portada']

class EditarLibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo','descripcion','portada','autores']