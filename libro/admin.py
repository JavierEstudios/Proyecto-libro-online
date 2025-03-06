from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from libro.models import *

class LectorLibroInLine(admin.TabularInline):
    model = Lector_Libro
    extra = 1

class UserAdmin(UserAdmin, admin.ModelAdmin):
    inlines = [LectorLibroInLine]

class LibroAdmin(admin.ModelAdmin):
    inlines = [LectorLibroInLine]
    ordering = ['titulo']

admin.site.register(Usuario, UserAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Capitulo)
admin.site.register(Genero)
