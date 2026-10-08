from django.contrib import admin
from .models import Especie, PacienteMascota

# Register your models here.

class  PacienteMascotaInline(admin.TabularInline):
    model = Especie
    extra = 1
    

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_clasificacion', 'activa', 'total_pacientes_asociados')
    search_fields = ('nombre', 'codigo_clasificacion')
    list_filter = ('activa' ,'codigo_clasificacion')
    
    @admin.display(description='Pacientes Asociados')
    def total_pacientes_asociados(self, obj):
        return obj.pacientes.count()
    
@admin.action(description='Dar de alta')
def dar_de_alta(modeladmin, request, queryset):
    filas_actualizadas = queryset.update(en_tratamiento = False)
    modeladmin.message_user(request, f'{filas_actualizadas} Pacietnes dados de alta.')
    
@admin.action(description='Ingresar a tratamiento')
def ingresar_a_tratamiento(modeladmin, request, queryset):
    filas_actualizadas = queryset.update(en_tratamiento = True)
    modeladmin.message_user(request, f'{filas_actualizadas} Ingresando a tratamiento.')


@admin.register(PacienteMascota)
class PacienteMascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre_mascota', 'nombre_dueno' , 'numero_chip', 'especie', 'peso_kg', 'en_tratamiento')
    search_fields = ('nombre_mascota', 'nombre_dueno', 'numero_chip', 'especie__nombre', 'especie__codigo_clasificacion')
    list_filter = ('en_tratamiento', 'especie', 'especie__codigo_clasificacion' , 'fecha_registro')
    list_editable = ['en_tratamiento']
    actions = [dar_de_alta, ingresar_a_tratamiento]

