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
        
class CapituloForm(forms.ModelForm):
    class Meta:
        model = Capitulo
        fields = ['titulo','numero','texto_principal','secuela_de']
        
class NuevoAutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['username', 'password', 'imagen_perfil', 'sobre_mi']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user
        
class EditarAutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['username', 'imagen_perfil', 'sobre_mi']
        
class NuevoLectorForm(forms.ModelForm):
    class Meta:
        model = Lector
        fields = ['username', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user
        
class EditarLectorForm(forms.ModelForm):
    class Meta:
        model = Lector
        fields = ['username']