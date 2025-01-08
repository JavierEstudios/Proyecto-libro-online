from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from libro.models import Usuario, Libro, Capitulo, Lector_Libro, Lector_Capitulo

class LectorLibroInLine(admin.TabularInline):
    model = Lector_Libro
    extra = 1

class LectorCapituloInLine(admin.TabularInline):
    model = Lector_Capitulo
    extra = 1
    
class UserAdmin(UserAdmin, admin.ModelAdmin):
    inlines = [LectorLibroInLine, LectorCapituloInLine]
    
class LibroAdmin(admin.ModelAdmin):
    inlines = [LectorLibroInLine]
    ordering = ['titulo']
    
class CapituloAdmin(admin.ModelAdmin):
    inlines = [LectorCapituloInLine]
    ordering = ['numero']

admin.site.register(Usuario, UserAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Capitulo, CapituloAdmin)
