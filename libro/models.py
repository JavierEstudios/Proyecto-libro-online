from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Usuario(AbstractUser):
    imagen_perfil = models.ImageField(blank=True, upload_to="fotos_de_perfil/")
    sobre_mi = models.CharField(max_length=2000)
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("usuario", kwargs={'pk':self.pk})

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=2000)
    portada = models.ImageField(blank=True, upload_to="portadas_libros/")
    inicio_publicacion = models.DateField(auto_now_add=True)
    fin_publicacion = models.DateField(null=True, blank=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="autor_libro")
    lectores = models.ManyToManyField(Usuario, related_name="lectores_libro", blank=True)
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("libro", kwargs={'pk':self.pk})
    
class Capitulo(models.Model):
    titulo = models.CharField(max_length=50)
    numero = models.IntegerField(default=1)
    texto_principal = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="autor_capitulo")
    lectores = models.ManyToManyField(Usuario, related_name="lectores_capitulo", blank=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    secuela_de = models.ManyToManyField("self", blank=True)
    def __str__(self):
        return f"{self.titulo} - {self.libro.titulo}"
    
    def get_absolute_url(self):
        return reverse("capitulo", kwargs={'pk':self.pk})
    