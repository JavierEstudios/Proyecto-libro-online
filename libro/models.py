from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Usuario(AbstractUser):
    imagen_perfil = models.ImageField(blank=True)
    sobre_mi = models.CharField(max_length=2000)
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("usuario", kwargs={'pk':self.pk})

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=2000)
    portada = models.ImageField(blank=True)
    inicio_publicacion = models.DateField(auto_now_add=True)
    fin_publicacion = models.DateField(blank=True)
    autores = models.ManyToManyField(Usuario, related_name="autor_libro")
    lectores = models.ManyToManyField(Usuario, through="Lector_Libro", related_name="lector_libro")
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
    lectores = models.ManyToManyField(Usuario, through="Lector_Capitulo", related_name="lector_capitulo")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    secuela_de = models.ManyToManyField("self")
    def __str__(self):
        return f"{self.titulo} - {self.libro.titulo}"
    
    def get_absolute_url(self):
        return reverse("capitulo", kwargs={'pk':self.pk})
    
class Lector_Libro(models.Model):
    CHOICES_RELACION = {"TBR": "Pendiente de Lectura",
                        "RDNG": "En proceso de Lectura",
                        "FNSH": "Lectura Finalizada"}
    relacion = models.CharField(choices=CHOICES_RELACION, max_length=4)
    favorito = models.BooleanField(default=False)
    lector = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="lector_libro_rel")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    
class Lector_Capitulo(models.Model):
    leido = models.BooleanField(default=False)
    lector = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="lector_capitulo_rel")
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE)
    