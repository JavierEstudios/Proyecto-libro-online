from django import forms
from .models import Usuario, Libro, Capitulo

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo','descripcion','portada']
        
class CapituloForm(forms.ModelForm):
    class Meta:
        model = Capitulo
        fields = ['titulo','numero','texto_principal','conexiones']

    #Propuesta de Jose Ignacio para filtrar los capitulos por el libro al que pertenecen, con algunas modificaciones
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        libro = kwargs.pop('libro', None)
        super().__init__(*args, **kwargs)
        self.fields['conexiones'].queryset = Capitulo.objects.filter(libro__pk=libro).exclude(pk=pk).distinct()

class NuevoUsuarioForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'imagen_perfil', 'sobre_mi']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user
        
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'imagen_perfil', 'sobre_mi']
