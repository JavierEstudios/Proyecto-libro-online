from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

class Usuario(AbstractUser):
    es_autor = models.BooleanField(default=False)
    es_lector = models.BooleanField(default=False)

class Autor(models.Model):
    imagen_perfil = models.ImageField(blank=True)
    sobre_mi = models.CharField(max_length=2000)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.usuario.username
    
    @receiver(models.signals.post_save, sender = Usuario)
    def crear_autor(sender, instance, created, **kwargs):
        if created:
            Autor.objects.create(user=instance)
    
    @receiver(models.signals.post_save, sender = Usuario)
    def guardar_autor(semder, instance, **kwargs):
        instance.autor.save()
    
class Lector(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.usuario.username
    
    @receiver(models.signals.post_save, sender = Usuario)
    def crear_lector(sender, instance, created, **kwargs):
        if created:
            Lector.objects.create(user=instance)
    
    @receiver(models.signals.post_save, sender = Usuario)
    def guardar_lector(semder, instance, **kwargs):
        instance.lector.save()

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=2000)
    portada = models.ImageField(blank=True)
    inicio_publicacion = models.DateField(auto_now_add=True)
    fin_publicacion = models.DateField(blank=True)
    autores = models.ManyToManyField(Autor)
    lectores = models.ManyToManyField(Lector, through="Lector_Libro")
    def __str__(self):
        return self.titulo
    
class Capitulo(models.Model):
    titulo = models.CharField(max_length=50)
    numero = models.IntegerField(default=1)
    texto_principal = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    lector = models.ManyToManyField(Lector, through="Lector_Capitulo")
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
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE)
    