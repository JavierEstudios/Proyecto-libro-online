from django import forms
from .models import Usuario, Autor, Libro, Capitulo

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
        
class NuevoUsuarioForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.es_autor = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user
        
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email']
        
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['imagen_perfil', 'sobre_mi']
        
AutorFormset = forms.modelformset_factory(Autor, form=AutorForm)