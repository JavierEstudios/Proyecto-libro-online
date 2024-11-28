from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from libro.models import Autor, Lector, Libro, Capitulo

admin.site.register(Autor, UserAdmin)
admin.site.register(Lector, UserAdmin)
admin.site.register(Libro)
admin.site.register(Capitulo)
