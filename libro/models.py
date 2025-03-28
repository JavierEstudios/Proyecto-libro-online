from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Usuario(AbstractUser):
    imagen_perfil = models.ImageField(blank=True, upload_to="fotos_de_perfil/")
    sobre_mi = models.CharField(max_length=2000)
    libros = models.ManyToManyField("Libro", through="Lector_Libro", related_name="lector", blank=True)
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("usuario", kwargs={'pk':self.pk})
    
class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=2000)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    portada = models.ImageField(blank=True, upload_to="portadas_libros/")
    inicio_publicacion = models.DateField(auto_now_add=True)
    fin_publicacion = models.DateField(null=True, blank=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("libro", kwargs={'pk':self.pk})
    
class Capitulo(models.Model):
    titulo = models.CharField(max_length=50)
    numero = models.IntegerField(default=1)
    texto_principal = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    lectores = models.ManyToManyField(Usuario, blank=True)
    conexiones = models.ManyToManyField("self", blank=True)
    def __str__(self):
        return f"{self.titulo} - {self.libro.titulo}"
    
class Lector_Libro(models.Model):
    CHOICES_RELACION = {"P": "Pendiente",
                        "L": "Leyendo",
                        "F": "Finalizado"}
    relacion = models.CharField(choices=CHOICES_RELACION, default="P", max_length=1)
    lector = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
