from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from libro.models import Usuario, Libro, Capitulo

admin.site.register(Usuario, UserAdmin)
admin.site.register(Libro)
admin.site.register(Capitulo)
