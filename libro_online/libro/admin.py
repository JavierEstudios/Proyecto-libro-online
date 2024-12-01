from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from libro.models import Autor, Lector, Libro, Capitulo, Lector_Libro

class LectorLibroInLine(admin.TabularInline):
    model = Lector_Libro
    extra = 1
    
class LectorAdmin(UserAdmin, admin.ModelAdmin):
    inlines = [LectorLibroInLine]
    
class LibroAdmin(admin.ModelAdmin):
    inlines = [LectorLibroInLine]

admin.site.register(Autor, UserAdmin)
admin.site.register(Lector, LectorAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Capitulo)
