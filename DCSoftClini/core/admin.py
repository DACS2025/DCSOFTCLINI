from django.contrib import admin
from .models import ContactoPaciente,Paciente,Especie,Raza,Tipodocid, HistoriaClinica, ConsultaMedica, Menumain, Menulist, TipoServicio,CitasProgramadas,EmpresaCliente,MedicoVeterinario,Parametros_sist


class TipodocidAdmin(admin.ModelAdmin):
    list_display = ('docid','desdocid')

admin.site.register(Tipodocid,TipodocidAdmin)

class ContactoPacienteAdmin(admin.ModelAdmin):
    list_display = ('tipo_contacto','nombre_primario','nombre_secundario','apellido_primario','apellido_secundario','docum_identidad','direccion','email','telef_fijo','telef_movil')

admin.site.register(ContactoPaciente,ContactoPacienteAdmin)

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre','contactopaciente','raza','sexo')

admin.site.register(Paciente,PacienteAdmin)


class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

admin.site.register(Especie,EspecieAdmin)

class RazaAdmin(admin.ModelAdmin):
    list_display = ('nombre','especie')

admin.site.register(Raza,RazaAdmin)

class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('nro_hiscli','paciente','anamnesis','antecedentes_medicos','vacunas_aplicadas','desparasitaciones')

admin.site.register(HistoriaClinica,HistoriaClinicaAdmin)

class ConsultaMedicaAdmin(admin.ModelAdmin):
    list_display = ('paciente','fecha','motivo','examen_fisico','diagnostico','tratamiento','notas_adicionales')

admin.site.register(ConsultaMedica,ConsultaMedicaAdmin)


class MenumainAdmin(admin.ModelAdmin):
    list_display = ('menucode','menuname','menu_menulist')

    def menu_menulist(self,obj):
        return ", ".join([c.submenuname for c in obj.menulist.all()])

admin.site.register(Menumain,MenumainAdmin)

class MenulistAdmin(admin.ModelAdmin):
    list_display = ('menusubcode','submenuname','menulink')

admin.site.register(Menulist,MenulistAdmin)

class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

admin.site.register(TipoServicio,TipoServicioAdmin)

from django.contrib import admin
from .models import CitasProgramadas, Tipodocid

@admin.register(CitasProgramadas)
class CitasProgramadasAdmin(admin.ModelAdmin):
    list_display = ('nombre_primario', 'apellido_primario', 'fecha_cita', 'hora_cita', 'paciente')
    search_fields = ('nombre_primario', 'apellido_primario', 'docum_identidad', 'paciente__nombre')
    list_filter = ('fecha_cita',)
    ordering = ('fecha_cita', 'hora_cita')

@admin.register(EmpresaCliente)
class EmpresaClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ruc', 'telefono', 'email', 'direccion','logo')
    search_fields = ('nombre', 'ruc', 'telefono', 'email', 'direccion','logo')

@admin.register(MedicoVeterinario)
class MedicoVeterinarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'numero_colegiatura', 'telefono', 'email', 'direccion')
    search_fields = ('nombres', 'numero_colegiatura', 'telefono', 'email', 'direccion')

@admin.register(Parametros_sist)
class Parametros_sistAdmin(admin.ModelAdmin):
    list_display = ('frecuencia_notificacion_cita',)
