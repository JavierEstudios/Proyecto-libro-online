from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from libro.models import Usuario, Autor, Lector, Libro, Capitulo, Lector_Libro, Lector_Capitulo

class AutorAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ("usuario__username", "usuario__email", "usuario__first_name", "usuario__last_name", "usuario__is_staff",)
    list_filter = ("usuario__is_staff", "usuario__is_superuser", "usuario__is_active", "usuario__groups",)
    ordering = ("usuario__username",)
    filter_horizontal = ()

class LectorLibroInLine(admin.TabularInline):
    model = Lector_Libro
    extra = 1

class LectorCapituloInLine(admin.TabularInline):
    model = Lector_Capitulo
    extra = 1
    
class LectorAdmin(UserAdmin, admin.ModelAdmin):
    inlines = [LectorLibroInLine, LectorCapituloInLine]
    list_display = ("usuario__username", "usuario__email", "usuario__first_name", "usuario__last_name", "usuario__is_staff",)
    list_filter = ("usuario__is_staff", "usuario__is_superuser", "usuario__is_active", "usuario__groups",)
    ordering = ("usuario__username",)
    filter_horizontal = ()
    
class LibroAdmin(admin.ModelAdmin):
    inlines = [LectorLibroInLine]
    ordering = ['titulo']
    
class CapituloAdmin(admin.ModelAdmin):
    inlines = [LectorCapituloInLine]
    ordering = ['numero']

admin.site.register(Usuario, UserAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Lector, LectorAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Capitulo, CapituloAdmin)
