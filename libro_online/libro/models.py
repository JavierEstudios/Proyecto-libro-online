from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    first_name = None
    last_name = None

class Autor(Usuario):
    imagen_perfil = models.ImageField(blank=True)
    sobre_mi = models.CharField(max_length=2000)
    def __str__(self):
        return self.username
    
class Lector(Usuario):
    def __str__(self):
        return self.username

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=2000)
    portada = models.ImageField(blank=True)
    inicio_publicacion = models.DateField()
    fin_publicacion = models.DateField(blank=True)
    autores = models.ManyToManyField(Autor)
    lectores = models.ManyToManyField(Lector, through="Lector_Libro")
    def __str__(self):
        return self.titulo
    
class Capitulo(models.Model):
    titulo = models.CharField(max_length=50)
    numero = models.IntegerField(default=1)
    texto_principal = models.TextField()
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    secuela_de = models.ManyToManyField("self")
    def __str__(self):
        return f"{self.titulo} - {self.libro.titulo}"
    
class Lector_Libro(models.Model):
    CHOICES_RELACION = {"TBR": "Pendiente de Lectura",
                        "RDNG": "En proceso de Lectura",
                        "FNSH": "Lectura Finalizada"}
    relacion = models.CharField(choices=CHOICES_RELACION, max_length=4)
    favorito = models.BooleanField(default=False)
    lector = models.ForeignKey(Lector, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    
class Lector_Capitulo(models.Model):
    leido = models.BooleanField(default=False)
    lector = models.ForeignKey(Lector, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    