from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Libro, Capitulo

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo','descripcion','genero','portada']
        
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
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'password2', 'email', 'imagen_perfil', 'sobre_mi']
    
    def clean_password(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        else:
            try:
                validate_password(password, user=None, password_validators=None)
            except forms.ValidationError as e:
                self.add_error('password', e)
            return password
    
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
        
class EditarContraseñaUsuarioForm(forms.ModelForm):
    opassword = forms.CharField(label='Contraseña antigua', widget=forms.PasswordInput)
    password = forms.CharField(label='Contraseña nueva', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['opassword','password', 'password2']
    
    def clean_password(self):
        opassword = self.cleaned_data['opassword']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if not self.instance.check_password(opassword):
            raise forms.ValidationError('La contraseña no es correcta')
        elif password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        else:
            try:
                validate_password(password, user=None, password_validators=None)
            except forms.ValidationError as e:
                self.add_error('password', e)
            return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
