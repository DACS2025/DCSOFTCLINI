from django.db import models
from django.utils import timezone
from datetime import date
import calendar
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

# Create your models here.
class Tipodocid(models.Model):
    docid =  models.CharField(max_length=1,verbose_name="Tipo documento de identidad")
    desdocid =  models.CharField(max_length=50,verbose_name="Descripción documento de identidad")
    def __str__(self):
        return f"{self.docid}-{self.desdocid}"

class ContactoPaciente(models.Model):
    TIPO_CONTACTO_CHOICES = [
        ('D', 'Dueño'),
        ('R', 'Responsable'),
    ]
    tipo_contacto = models.CharField(max_length=1,choices=TIPO_CONTACTO_CHOICES,default='D')
    nombre_primario = models.CharField(max_length=50,verbose_name='Primer nombre')    
    nombre_secundario = models.CharField(max_length=50,verbose_name='Segundo nombre',blank=True)
    apellido_primario = models.CharField(max_length=50,verbose_name='Primer apellido')    
    apellido_secundario = models.CharField(max_length=50,verbose_name='Segundo apellido',blank=True)
    nombres = models.CharField(max_length=200,verbose_name='Nombres',blank=True)
    tipodocid = models.ForeignKey(Tipodocid,verbose_name="Tipo documento de identidad",on_delete=models.PROTECT,default='')
    docum_identidad = models.CharField(max_length=20,verbose_name='Documento de identidad')
    direccion = models.CharField(max_length=100,verbose_name='Dirección')
    email = models.CharField(max_length=100,verbose_name='Email',blank=True)
    telef_fijo = models.CharField(max_length=20,verbose_name='Telef. Fijo',blank=True)
    telef_movil = models.CharField(max_length=20,verbose_name='Movil',blank=True)

    def __str__(self):
        return f"{self.nombres} (docId {self.docum_identidad} {self.direccion} tel.fijo {self.telef_fijo} tel.movil {self.telef_movil})"

    def save(self, *args, **kwargs):
            # Validar campos ForeignKey si es_loteproducto es True
            nombre_primario = self.nombre_primario.strip()
            nombre_secundario = self.nombre_secundario.strip()
            apellido_primario = self.apellido_primario.strip()
            apellido_secundario = self.apellido_secundario.strip()

            nombres = ""
            if not nombre_primario == "":
                nombres = nombre_primario

            if not nombre_secundario == "":
                nombres += " "+nombre_secundario

            if not apellido_primario == "":
                nombres += " "+apellido_primario

            if not apellido_secundario == "":
                nombres += " "+apellido_secundario

            self.nombres = nombres
            
            # Llamar al método save original
            super().save(*args, **kwargs)

class Especie(models.Model):
    nombre = models.CharField(max_length=100,verbose_name='Especie')
    class Meta:
        unique_together = ('nombre',)
        ordering = ['nombre',]
    def __str__(self):
        return f"{self.nombre}"

class Raza(models.Model):
    nombre = models.CharField(max_length=100,verbose_name='Raza',blank=True)
    especie = models.ForeignKey(Especie,on_delete=models.PROTECT,verbose_name="Especie",default=1)
    class Meta:
        unique_together = ('especie','nombre')
        ordering = ['especie','nombre',]

    def __str__(self):
        return f"{self.especie.nombre}-{self.nombre}"

class Paciente(models.Model):
    MACHO = 'M'
    HEMBRA = 'H'
    SEX_CHOICES = [
        (MACHO, 'Macho'),
        (HEMBRA, 'Hembra'),
    ]
    nombre = models.CharField(max_length=20,verbose_name='Nombre')
    contactopaciente = models.ForeignKey(ContactoPaciente,verbose_name="Contacto", on_delete=models.PROTECT, default=None,null=True,related_name='paciente')
    raza = models.ForeignKey(Raza,verbose_name="Raza", on_delete=models.PROTECT, default=None,null=True)
    sexo =  models.CharField(max_length=1,choices=SEX_CHOICES,default='M')
    nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    color = models.CharField(max_length=50,verbose_name='color / tipo de pelaje',blank=True,default='')
    peso = models.DecimalField(max_digits=13, decimal_places=2,verbose_name='Peso en KG',blank=True,default=0)
    fecha = models.DateField(default=date.today)
    fecha_act_peso = models.DateField(default=date.today)
    chip = models.CharField(max_length=50,verbose_name='Chip #',blank=True,default='')
    imagen = models.ImageField(upload_to='projects', blank=True, null=True,default=None)  # Nuevo campo de imagen

    class Meta:
        unique_together = ('nombre','contactopaciente',)
        ordering = ['nombre','contactopaciente__nombres']

    def calcular_edad_detallada(self):
        today = date.today()
        years = today.year - self.nacimiento.year
        months = today.month - self.nacimiento.month
        days = today.day - self.nacimiento.day

        # Ajustar si el cumpleaños aún no ha ocurrido en el mes actual
        if months < 0 or (today.month == self.nacimiento.month and today.day < self.nacimiento.day):
            years -= 1
            months += 12

        # Ajustar si el día de nacimiento aún no ha ocurrido en el mes actual
        if days < 0:
            months -= 1
            prev_month = (today.month - 1) if today.month > 1 else 12
            # Obtener el último día del mes anterior
            days_in_prev_month = calendar.monthrange(today.year, prev_month)[1]
            days += days_in_prev_month        

        # Formatear el resultado como una cadena
        edad = []
        if years > 0:
            edad.append(f"{years} año{'s' if years > 1 else ''}")
        if months > 0:
            edad.append(f"{months} mes{'es' if months > 1 else ''}")
        if days > 0:
            edad.append(f"{days} día{'s' if days > 1 else ''}")
        
        return " ".join(edad)

    def mostrar_peso_inicial_actual(self):

        paciente = Paciente.objects.get(id=self.id)
        consultas = ConsultaMedica.objects.filter(paciente=paciente).order_by("-fecha","-id")
        consultamedica = consultas.first()
        consultamedica_anterior = consultas.exclude(id=consultamedica.id).first() if consultamedica else None

        pesos = ""
        if consultamedica:
            pesos = "Ult:   " + str(consultamedica.peso)+" kg"
            if consultamedica_anterior:
                pesos = pesos + " Ant:"+str(consultamedica_anterior.peso)+" kg"
            elif self.peso:
                pesos = pesos + " Ant:"+str(self.peso)+" kg"
        elif paciente:
            pesos = "Ult:"+str(self.peso)+" kg"

        return pesos

    def __str__(self):
        if self.contactopaciente.tipo_contacto=='D':
            tipocontacto = 'Dueño'
        else:
            tipocontacto = 'Responsable'

        return f"{self.nombre} - (contacto {self.contactopaciente.nombres} - {tipocontacto})"

    def save(self, *args, **kwargs):
        self.fecha = timezone.now().date()
        super(Paciente, self).save(*args,**kwargs)

class HistoriaClinica(models.Model):
    nro_hiscli = models.CharField(max_length=10,verbose_name="Nro. Historia Clinica",blank=True, null=True)
    fecha = models.DateField(default=date.today)
    paciente = models.OneToOneField(Paciente, on_delete=models.PROTECT,verbose_name="Paciente",related_name="historia")
    anamnesis = models.TextField(verbose_name="Anamnesis")
    antecedentes_medicos = models.TextField(blank=True, null=True,verbose_name="Antecedentes medicos")
    vacunas_aplicadas = models.TextField(blank=True, null=True,verbose_name="Vacunas aplicadas")
    desparasitaciones = models.TextField(blank=True, null=True,verbose_name="Desparasitaciones")
    medicamentos_actuales = models.TextField(blank=True, null=True,verbose_name="Medicamentos actuales")

    def __str__(self):
        return f"Historia Clínica de {self.paciente.nombre} - nro HC {self.nro_hiscli}"
    
    def save(self, *args, **kwargs):
        if not self.nro_hiscli:
            last_nro_hiscli = HistoriaClinica.objects.all().order_by('-nro_hiscli').first()
            if last_nro_hiscli:
                numerostr = last_nro_hiscli.nro_hiscli
                last_number = int(numerostr)
                new_number = last_number + 1
            else:
                new_number = 1

            self.nro_hiscli = f"{new_number:06d}"

        super().save(*args, **kwargs)

class MedicoVeterinario(models.Model):
    nombres = models.CharField(max_length=100,verbose_name="Nombre del veterinario")
    numero_colegiatura = models.CharField(max_length=20,verbose_name="Número de colegiatura")
    direccion = models.CharField(max_length=100,verbose_name="Dirección")
    email = models.CharField(max_length=100,verbose_name="EMAIL")
    telefono = models.CharField(max_length=100,verbose_name="Teléfonos")
    def __str__(self):
        return self.nombres + "(CMVP"+self.numero_colegiatura+")"

class ConsultaMedica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,related_name='consultas')
    fecha = models.DateField(default=date.today)
    peso = models.DecimalField(max_digits=13, decimal_places=2,verbose_name='Peso en KG',blank=True,default=0)
    motivo = models.TextField()
    examen_fisico = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    notas_adicionales = models.TextField(blank=True, null=True)
    medicoveterinario = models.ForeignKey(MedicoVeterinario,models.PROTECT,verbose_name="Medico veterinario Dr",blank=True,null=True,default=1)

    def __str__(self):
        return f"Consulta de {self.paciente.nombre} del {self.fecha.strftime('%Y-%m-%d')}"

class RecetaMedica(models.Model):
    consultamedica = models.ForeignKey(ConsultaMedica,models.CASCADE,verbose_name="Consulta Medica")
    farmaco = models.CharField(max_length=100,verbose_name="Farmaco")
    cantidad = models.CharField(max_length=100,verbose_name="Cantidad")
    dosis = models.CharField(max_length=100,verbose_name="Dosis")

class Menulist(models.Model):
    menusubcode = models.IntegerField(default=0)
    submenuname = models.CharField(max_length=100)
    menulink = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Detalle lista Menu'
        verbose_name_plural = 'Detalles listas Menu'
        ordering = ['menusubcode']

    def __str__(self):
        return self.submenuname

class Menumain(models.Model):
    menucode = models.IntegerField()
    menuname = models.CharField(max_length=100)
    menulist = models.ManyToManyField(Menulist,verbose_name='Sub menú',related_name='get_Menumain',blank=True)
 
    class Meta:
        verbose_name = 'Lista Menu'
        verbose_name_plural = 'Lista Menu'
        ordering = ['menucode']

    def __str__(self):
        return self.menuname

class Moneda(models.Model):
    simbolo = models.CharField(max_length=10, verbose_name="Simbolo") 
    nombre = models.CharField(max_length=100, verbose_name="Moneda") 
    def __str__(self):
        return self.simbolo - self.nombre

class TipoServicio(models.Model):
    CLINICO = 'C'
    NOCLINICO = 'S'
    CATEGORIA_CHOICES = [
        (CLINICO, 'Clinico'),
        (NOCLINICO, 'Servicios complementarios'),
    ]

    categoria = models.CharField(max_length=1,choices=CATEGORIA_CHOICES,default='C')
    nombre = models.CharField(max_length=100, verbose_name="Nombre del servicio")
    precio = models.DecimalField(max_digits=13, decimal_places=2, verbose_name='Precio del servicio',default=0)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, verbose_name="Moneda",blank=True,null=True)
    class Meta:
        unique_together = ('categoria','nombre')
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Servicios(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente",related_name="servicios")
    fecha = models.DateField(default=date.today, verbose_name="Fecha del servicio")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas adicionales")
    class Meta:
        ordering = ['paciente__historia__nro_hiscli','paciente',]

    def __str__(self):
        return f"Servicio para {self.paciente.nombre} del {self.fecha.strftime('%Y-%m-%d')}"

class ServiciosDetalle(models.Model):
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name="Servicio",related_name="servicios_detalle")
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE, verbose_name="Tipo de servicio")

    def __str__(self):
        return f"Detalle de servicio: {self.tipo_servicio.nombre} para {self.servicio.paciente.nombre}"

class Notificacion(models.Model):
    nota = models.TextField(verbose_name="Nota")
    fecha_inicio = models.DateField(verbose_name="Fecha Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha Fin")
    hora_notificacion = models.TimeField(verbose_name="Hora de Notificación")

    def __str__(self):
        return f"Notificación: {self.nota[:30]}..."  # Muestra los primeros 30 caracteres de la nota

class CitasProgramadas(models.Model):
    # Información del Cliente
    nombre_primario = models.CharField(max_length=50, verbose_name='Primer nombre')
    nombre_secundario = models.CharField(max_length=50, verbose_name='Segundo nombre', blank=True)
    apellido_primario = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido_secundario = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True)
    tipodocid = models.ForeignKey(Tipodocid, verbose_name="Tipo documento de identidad", on_delete=models.PROTECT, default=None)
    docum_identidad = models.CharField(max_length=20, verbose_name='Documento de identidad')
    telef_fijo = models.CharField(max_length=20, verbose_name='Teléfono Fijo', blank=True)
    telef_movil = models.CharField(max_length=20, verbose_name='Teléfono Móvil', blank=True)

    # Información de la Cita
    fecha_cita = models.DateField(verbose_name='Fecha de la Cita', default=date.today)
    hora_cita = models.TimeField(verbose_name='Hora de la Cita')
    notas = models.TextField(verbose_name='Notas adicionales', blank=True, null=True)

    # Relación con el Paciente (opcional para clientes ya registrados)
    paciente = models.ForeignKey(
        'Paciente', 
        verbose_name='Paciente registrado', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ['-fecha_cita','-hora_cita']

    def __str__(self):
        return f"Cita para {self.nombre_primario} {self.apellido_primario} - Fecha: {self.fecha_cita}, Hora: {self.hora_cita}"

    def save(self, *args, **kwargs):

        paciente = self.paciente

        print("paciente",paciente)

        if paciente:
            contactopaciente_id = paciente.contactopaciente.id
            contactopaciente = get_object_or_404(ContactoPaciente, pk=contactopaciente_id)
            
            nombre_primario = contactopaciente.nombre_primario
            nombre_secundario = contactopaciente.nombre_secundario
            apellido_primario = contactopaciente.apellido_primario
            apellido_secundario = contactopaciente.apellido_secundario

            # Asignar el valor de cada campo
            
            self.nombre_primario = nombre_primario
            self.nombre_secundario = nombre_secundario
            self.apellido_primario = apellido_primario
            self.apellido_secundario = apellido_secundario

        super().save(*args, **kwargs)

class EmpresaCliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Razon social')
    ruc = models.CharField(max_length=11, verbose_name='RUC')
    telefono = models.CharField(max_length=100, verbose_name='Telefono')
    email = models.CharField(max_length=100, verbose_name='Email')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    logo = models.ImageField(upload_to='projects', blank=True, null=True,default=None)  # Nuevo campo de imagen

class Parametros_sist(models.Model):
    frecuencia_notificacion_cita = models.IntegerField(verbose_name='Frecuencia de notificación de cita (en mili segundos)',default=30)