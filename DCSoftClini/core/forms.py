from django import forms
from .models import ContactoPaciente, Paciente, Especie, Raza, Tipodocid, HistoriaClinica, ConsultaMedica, TipoServicio, Servicios, ServiciosDetalle,CitasProgramadas,EmpresaCliente,MedicoVeterinario

class TipodocidForm(forms.ModelForm):
    class Meta:
        model = Tipodocid
        fields = ['docid','desdocid']
        widgets = {
            'docid':forms.TextInput(attrs={'class':'form-control'}),
            'desdocid':forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'docid':'Tipo de documento de identidad',
            'desdocid':'Descripción del tipo de documento de identidad'
        }

class ContactoPacienteForm(forms.ModelForm):
    class Meta:
        model = ContactoPaciente
        fields = ['id','tipo_contacto','nombre_primario','nombre_secundario','apellido_primario','apellido_secundario','tipodocid','docum_identidad','direccion','email','telef_fijo','telef_movil']
        widgets = {
            'tipo_contacto': forms.Select(attrs={'class':'form-control'}),
            'nombre_primario': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_secundario': forms.TextInput(attrs={'class':'form-control'}),
            'apellido_primario': forms.TextInput(attrs={'class':'form-control'}),
            'apellido_secundario': forms.TextInput(attrs={'class':'form-control'}),
            'tipodocid': forms.Select(attrs={'class':'form-control'}),
            'docum_identidad': forms.TextInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'telef_fijo': forms.TextInput(attrs={'class':'form-control'}),
            'telef_movil': forms.TextInput(attrs={'class':'form-control'}),
        }

        labels = {
            'nombre_primario': 'Primer nombre',
            'nombre_secundario': 'Segundo nombre',
            'apellido_primario': 'Primer apellido',
            'apellido_secundario': 'Segundo apellido',
            'tipodocid': 'Tipo de documento de Identidad',
            'docum_identidad': 'Documento de Identidad',
            'direccion': 'Dirección de domicilio',
            'email': 'correo electrónico',
            'telef_fijo': 'Teléfono fijo',
            'telef_movil': 'Teléfono móvil',
        }

class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ['id','contactopaciente','nombre','raza','sexo','nacimiento','color','peso','chip','imagen']
        widgets = {
            'contactopaciente': forms.Select(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'raza': forms.Select(attrs={'class':'form-control'}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
            'nacimiento': forms.TextInput(attrs={'class':'form-control'}),
            'color': forms.TextInput(attrs={'class':'form-control'}),
            'peso': forms.TextInput(attrs={'class':'form-control'}),
            'chip': forms.TextInput(attrs={'class':'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
        }
        labels = {
            'contactopaciente': 'Contacto',
            'nombre': 'Paciente',
            'raza': 'Especie-Raza',
            'sexo': 'Sexo',
            'nacimiento': 'Fecha de nacimiento',
            'color': 'Color',
            'peso': 'Peso Kg',
            'chip': 'Chip',
            'imagen': 'Imagen del paciente',
        }

class PacienteUpdateForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ['id','contactopaciente','nombre','raza','sexo','nacimiento','color','peso','chip','imagen']
        widgets = {
            'contactopaciente': forms.Select(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'raza': forms.Select(attrs={'class':'form-control'}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
            'nacimiento': forms.TextInput(attrs={'class':'form-control'}),
            'color': forms.TextInput(attrs={'class':'form-control'}),
            'peso': forms.TextInput(attrs={'class':'form-control'}),
            'chip': forms.TextInput(attrs={'class':'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
        }
        labels = {
            'contactopaciente': 'Contacto',
            'nombre': 'Paciente',
            'raza': 'Especie-Raza',
            'sexo': 'Sexo',
            'nacimiento': 'Fecha de nacimiento',
            'color': 'Color',
            'peso': 'Peso Kg',
            'chip': 'Chip',
            'imagen': 'Imagen del paciente',
        }
    def __init__(self, *args, **kwargs):
        super(PacienteUpdateForm, self).__init__(*args, **kwargs)
        self.fields['contactopaciente'].widget.attrs['disabled'] = 'disabled'

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['id','nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
        }

class RazaForm(forms.ModelForm):
    class Meta:
        model = Raza
        fields = ['id','especie','nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'especie': forms.Select(attrs={'class':'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'especie': 'Especie',
        }

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = [
            'paciente','anamnesis', 'antecedentes_medicos',
            'vacunas_aplicadas', 'desparasitaciones', 'medicamentos_actuales'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'anamnesis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'antecedentes_medicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'vacunas_aplicadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'desparasitaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
        }
        labels = {
            'paciente': 'Paciente',
            'anamnesis': 'Anamnesis',
            'antecedentes_medicos': 'Antecedentes médicos',
            'vacunas_aplicadas': 'Vacunas aplicadas',
            'desparasitaciones': 'Desparasitaciones',
            'medicamentos_actuales': 'Medicamentos actuales',
        }

class HistoriaClinicaUpdateForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = [
            'nro_hiscli','paciente','anamnesis', 'antecedentes_medicos',
            'vacunas_aplicadas', 'desparasitaciones', 'medicamentos_actuales'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'anamnesis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'antecedentes_medicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'vacunas_aplicadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'desparasitaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
        }
        labels = {
            'paciente': 'Paciente',
            'anamnesis': 'Anamnesis',
            'antecedentes_medicos': 'Antecedentes médicos',
            'vacunas_aplicadas': 'Vacunas aplicadas',
            'desparasitaciones': 'Desparasitaciones',
            'medicamentos_actuales': 'Medicamentos actuales',
        }

    def __init__(self, *args, **kwargs):
        super(HistoriaClinicaUpdateForm, self).__init__(*args, **kwargs)
        self.fields['nro_hiscli'].widget.attrs['disabled'] = 'disabled'
        self.fields['paciente'].widget.attrs['disabled'] = 'disabled'

class HistoriaClinicaDetailForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = [
            'paciente','nro_hiscli','fecha', 'anamnesis', 'antecedentes_medicos',
            'vacunas_aplicadas', 'desparasitaciones', 'medicamentos_actuales'
        ]
        widgets = {
            'nro_hiscli': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'anamnesis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'style': 'resize: vertical;'}),
            'antecedentes_medicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'style': 'resize: vertical;'}),
            'vacunas_aplicadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'style': 'resize: vertical;'}),
            'desparasitaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'style': 'resize: vertical;'}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'style': 'resize: vertical;'}),
        }
        labels = {
            'nro_hiscli': 'Nro. Historia Clinica',
            'fecha': 'Fecha',
            'paciente': 'Paciente',
            'anamnesis': 'Anamnesis',
            'antecedentes_medicos': 'Antecedentes médicos',
            'vacunas_aplicadas': 'Vacunas aplicadas',
            'desparasitaciones': 'Desparasitaciones',
            'medicamentos_actuales': 'Medicamentos actuales',
        }

    def __init__(self, *args, **kwargs):
        super(HistoriaClinicaDetailForm, self).__init__(*args, **kwargs)
        self.fields['nro_hiscli'].widget.attrs['disabled'] = 'disabled'
        self.fields['fecha'].widget.attrs['disabled'] = 'disabled'
        self.fields['paciente'].widget.attrs['disabled'] = 'disabled'
        self.fields['anamnesis'].widget.attrs['disabled'] = 'disabled'
        self.fields['antecedentes_medicos'].widget.attrs['disabled'] = 'disabled'
        self.fields['vacunas_aplicadas'].widget.attrs['disabled'] = 'disabled'
        self.fields['desparasitaciones'].widget.attrs['disabled'] = 'disabled'
        self.fields['medicamentos_actuales'].widget.attrs['disabled'] = 'disabled'


class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica

        fields = ['paciente','fecha','peso','motivo','examen_fisico','diagnostico','tratamiento','notas_adicionales','medicoveterinario']
        
        widgets = {
            'paciente': forms.Select(attrs={'class':'form-control'}),
            'fecha': forms.TextInput(attrs={'class':'form-control'}),
            'peso': forms.TextInput(attrs={'class':'form-control'}),
            'motivo': forms.Textarea(attrs={'class':'form-control', 'rows': 2, 'style': 'resize: vertical;'}),
            'examen_fisico': forms.Textarea(attrs={'class':'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'diagnostico': forms.Textarea(attrs={'class':'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'tratamiento': forms.Textarea(attrs={'class':'form-control', 'rows': 3, 'style': 'resize: vertical;'}),
            'notas_adicionales': forms.Textarea(attrs={'class':'form-control', 'rows': 1, 'style': 'resize: vertical;'}),
            'medicoveterinario': forms.Select(attrs={'class':'form-control'}),
        }
        labels = {
            'paciente': 'Paciente',
            'fecha': 'Fecha',
            'peso': 'Peso paciente',
            'motivo': 'Motivo de consulta',
            'examen_fisico': 'Examen físico',
            'diagnostico': 'Diagnostico',
            'tratamiento': 'Tratamiento',
            'notas_adicionales': 'Notas adicionales',
            'medicoveterinario': 'Medico veterinario Dr',
        }
    def __init__(self, *args, **kwargs):
        super(ConsultaMedicaForm, self).__init__(*args, **kwargs)
        paciente_id = kwargs.get('initial', {}).get('paciente')
        if paciente_id:
            self.fields['paciente'].widget.attrs['disabled'] = 'disabled'

class SeleccionarServiciosForm(forms.Form):
    tipos_servicio = forms.ModelMultipleChoiceField(
        queryset=TipoServicio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Marque los servicios a brindar"
    )
    notas = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Notas adicionales",
        required=False
    )
    fecha = forms.CharField(
        widget=forms.TextInput(),
        label="Fecha",
        required=True
    )
    
class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio

        fields = ['categoria','nombre','precio','moneda']
        
        widgets = {
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(attrs={'class':'form-control'}),
        }
        labels = {
            'categoria': 'Categoria',
            'nombre': 'Servicio',
            'precio': 'Precio',
            'moneda': 'Moneda',
        }


class CitasProgramadasForm(forms.ModelForm):
    class Meta:
        model = CitasProgramadas
        fields = [
            'paciente',
            'tipodocid', 'docum_identidad', 
            'telef_movil', 
            'fecha_cita', 'hora_cita', 
            'notas'
        ]

        widgets = {
            'paciente': forms.Select(attrs={'class':'form-control'}),
            'tipodocid': forms.Select(attrs={'class':'form-control'}),
            'docum_identidad': forms.TextInput(attrs={'class':'form-control'}),
            'telef_movil': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_cita': forms.TextInput(attrs={'class':'form-control'}),
            'hora_cita': forms.TextInput(attrs={'class':'form-control'}),
            'notas': forms.Textarea(attrs={'class':'form-control','rows': 4, 'style': 'resize: vertical;'})
        }

        labels = {
            'paciente': 'Paciente',
            'tipodocid': 'Documento de Identidad (contacto)',
            'docum_identidad': 'Nro. Documento de Identidad (contacto)',
            'telef_movil': 'Teléfono',
            'fecha_cita': 'Reserva fecha de cita',
            'hora_cita': 'Reserva hora de cita',
            'notas': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super(CitasProgramadasForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].widget.attrs['disabled'] = 'disabled'
        self.fields['tipodocid'].widget.attrs['disabled'] = 'disabled'
        self.fields['docum_identidad'].widget.attrs['disabled'] = 'disabled'
        self.fields['telef_movil'].widget.attrs['disabled'] = 'disabled'

class CitasProgramadasNuevoPacienteForm(forms.ModelForm):
    class Meta:
        model = CitasProgramadas
        fields = [
            'nombre_primario', 
            'apellido_primario', 'apellido_secundario', 
            'tipodocid', 'docum_identidad', 
            'telef_movil', 
            'fecha_cita', 'hora_cita', 
            'notas'
        ]

        widgets = {
            'nombre_primario': forms.TextInput(attrs={'class':'form-control'}),
            'apellido_primario': forms.TextInput(attrs={'class':'form-control'}),
            'apellido_secundario': forms.TextInput(attrs={'class':'form-control'}),
            'tipodocid': forms.Select(attrs={'class':'form-control'}),
            'docum_identidad': forms.TextInput(attrs={'class':'form-control'}),
            'telef_movil': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_cita': forms.TextInput(attrs={'class':'form-control'}),
            'hora_cita': forms.TextInput(attrs={'class':'form-control'}),
            'notas': forms.Textarea(attrs={'class':'form-control','rows': 2, 'style': 'resize: vertical;'}),
        }

        labels = {
            'nombre_primario': 'Primer nombre',
            'apellido_primario': 'Primer apellido',
            'apellido_secundario': 'Segundo apellido',
            'tipodocid': 'Tipo de documento de Identidad',
            'docum_identidad': 'Documento de Identidad',
            'telef_movil': 'Teléfono',
            'fecha_cita': 'Reserva fecha de cita',
            'hora_cita': 'Reserva hora de cita',
            'notas': 'Notas',
        }

class EmpresaClienteForm(forms.ModelForm):
    class Meta:
        model = EmpresaCliente
        fields = ['id','nombre','ruc','telefono','email','direccion','logo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'ruc': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
        }
        labels = {
            'nombre': 'Razon social',
            'ruc': 'RUC',
            'telefono': 'Telefono',
            'email': 'Email',
            'direccion': 'Domicilio',
            'logo': 'Logo de la empresa',
        }

class MedicoVeterinarioForm(forms.ModelForm):
    class Meta:
        model = MedicoVeterinario
        fields = ['id','nombres','numero_colegiatura','telefono','email','direccion']
        widgets = {
            'nombres': forms.TextInput(attrs={'class':'form-control'}),
            'numero_colegiatura': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'nombres': 'Nombres',
            'numero_colegiatura': 'Número de colegiatura',
            'telefono': 'Telefono',
            'email': 'Email',
            'direccion': 'Domicilio',
        }

