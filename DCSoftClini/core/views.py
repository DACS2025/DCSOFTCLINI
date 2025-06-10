from django.http import JsonResponse
from django.views.generic import FormView
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.urls import reverse, reverse_lazy
from .forms import PacienteForm, ContactoPacienteForm, HistoriaClinicaForm,ConsultaMedicaForm,HistoriaClinicaDetailForm,SeleccionarServiciosForm,CitasProgramadasForm,MedicoVeterinarioForm,TipoServicioForm,EspecieForm,RazaForm,PacienteUpdateForm,HistoriaClinicaUpdateForm,CitasProgramadasNuevoPacienteForm
from .models import HistoriaClinica,Menumain, Paciente, ContactoPaciente,ConsultaMedica,Servicios,ServiciosDetalle,CitasProgramadas,EmpresaCliente,RecetaMedica,MedicoVeterinario,TipoServicio,Especie,Raza
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from core.utils import encode_id, decode_id
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.http import FileResponse, HttpResponse
from core.document_formats import generar_historia_clinica
import os
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from weasyprint import HTML
from django.template.loader import render_to_string
import base64
import webbrowser

@login_required
def home(request):
    menumain = Menumain.objects.all()
    return render(request,'core/home.html',{'menumain':menumain})

@login_required
def historia_clinica(request):
    historiaclinica = HistoriaClinica.objects.all()
    return render(request,'core/historia_clinica_list.html',{'historiaclinica':historiaclinica})

class PacienteListView(ListView):
    model = Paciente
    paginate_by = 12  # Número de elementos por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.request.session.get("pacienteListview_paciente_id", None)
        if paciente_id:
            try:
                # Obtener el paciente relacionado con nro_hiscli
                #paciente = Paciente.objects.get(historia__nro_hiscli=nro_hiscli)
                paciente = Paciente.objects.get(id=paciente_id)

                context['paciente_id'] = paciente.id

                # Obtener el contacto relacionado con el paciente
                contacto_nombre = paciente.contactopaciente.nombres
                
                # Obtener pacientes que cumplen el orden lógico deseado
                pacientes_filtrados = Paciente.objects.filter(
                    Q(nombre__lt=paciente.nombre) |  # Pacientes con nombre menor (alfabéticamente)
                    Q(nombre=paciente.nombre, contactopaciente__nombres__lte=contacto_nombre)  # Pacientes con el mismo nombre pero contacto menor o igual
                ).order_by('nombre', 'contactopaciente__nombres')

                # Contar la cantidad total de pacientes
                contador_pacientes = pacientes_filtrados.count()
                                
                # Calcular el número de página correspondiente
                page_number = 1

                if (contador_pacientes) > self.paginate_by and ((contador_pacientes) % self.paginate_by) != 0: 
                    page_number = (contador_pacientes) // self.paginate_by + 1 
                elif (contador_pacientes) > self.paginate_by and ((contador_pacientes) % self.paginate_by) == 0:
                    page_number = (contador_pacientes) // self.paginate_by

                context['page_number'] = page_number  # Este valor se usará en el template y el JS
                # Eliminamos la variable para que este proceso se ejecute solo una vez
                self.request.session.pop("pacienteListview_paciente_id", None)
            except Paciente.DoesNotExist:
                # Si no se encuentra el paciente, marcar como None
                context['page_number'] = None
                context['paciente_id'] = None
        else:
            context['page_number'] = None
            context['paciente_id'] = None

        # Codificar IDs para las historias clínicas asociadas
        pacientes = context.get('object_list', [])
        for paciente in pacientes:
            if hasattr(paciente, 'historia') and paciente.historia is not None:
                paciente.historia.encoded_id = encode_id(paciente.historia.id)
                print(paciente.historia.encoded_id)
            else:
                paciente.encoded_id = encode_id(paciente.id)

        return context

class PacienteCreateView(CreateView):
    model: Paciente
    form_class = PacienteForm
    template_name = "core/paciente_form.html"

    def get_initial(self):
        initial = super().get_initial()
        contactopaciente_id = self.kwargs.get('contactopaciente_id')
        if contactopaciente_id:
            initial['contactopaciente'] = contactopaciente_id
        return initial

    def get_success_url(self):
        #return reverse('pacientes')
        self.request.session["pacienteListview_paciente_id"] = self.object.id
        encoded_id = encode_id(self.object.id)
        return reverse('historia_add', kwargs={'encoded_id': encoded_id})

    def form_valid(self, form):
            response = super().form_valid(form)
            return redirect(self.get_success_url())

class PacienteUpdate(UpdateView):
    model = Paciente
    form_class = PacienteUpdateForm
    template_name_suffix = "_update_form"

    def get_initial(self):
        initial = super().get_initial()
        paciente_id = self.kwargs.get('pk')
        self.request.session["pacienteListview_paciente_id"] = paciente_id
        return initial

    def get_success_url(self):
        return reverse_lazy('paciente_update', args=[self.object.id]) + "?ok"

class ContactoPacienteCreateView(CreateView):
    model = ContactoPaciente
    form_class = ContactoPacienteForm
    template_name = "core/contactopaciente_form.html"

    def get_success_url(self):
        return reverse('paciente_add_id', kwargs={'contactopaciente_id': self.object.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

class ContactoPacienteUpdate(UpdateView):
    model = ContactoPaciente
    form_class = ContactoPacienteForm
    template_name_suffix = "_update_form"

    def get_initial(self):
        initial = super().get_initial()
        paciente_id = self.kwargs.get('paciente_id')
        self.request.session["pacienteListview_paciente_id"] = paciente_id
        return initial

    def get_success_url(self):
        paciente_id = self.kwargs.get('paciente_id')
        return reverse_lazy('contactopaciente_update', args=[self.object.id,paciente_id]) + "?ok"


class HistoriaClinicaCreateView(CreateView):
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = "core/historiaclinica_form.html"

    def get_success_url(self):
        self.request.session["pacienteListview_paciente_id"] = self.object.paciente.id
        return reverse('pacientes')

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        encoded_id = self.kwargs.get('encoded_id')
        paciente_id = decode_id(encoded_id)
        initial['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        self.request.session["pacienteListview_paciente_id"] = paciente_id
        return initial

class HistoriaClinicaUpdate(UpdateView):
    model = HistoriaClinica
    form_class = HistoriaClinicaUpdateForm
    template_name_suffix = "_update_form"

    def get_initial(self):
        initial = super().get_initial()
        historia_id = self.kwargs.get('pk')
        historia = HistoriaClinica.objects.get(id=historia_id)
        paciente_id = historia.paciente.id
        self.request.session["pacienteListview_paciente_id"] = paciente_id
        return initial

    def get_success_url(self):
        return reverse_lazy('historia_update', args=[self.object.id]) + "?ok"

class ConsultaMedicaCreateView(CreateView):
    model = ConsultaMedica
    form_class = ConsultaMedicaForm
    template_name = "core/consultamedica_form.html"

    def get_success_url(self):
        #return reverse('pacientes_nro_hiscli', kwargs={'nro_hiscli': self.object.paciente.historia.nro_hiscli})
        return reverse('posologia_add', kwargs={'consultamedica_id': self.object.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        nro_hiscli = self.kwargs.get('nro_hiscli')
        historia = get_object_or_404(HistoriaClinica, nro_hiscli=nro_hiscli)
        initial['paciente'] = get_object_or_404(Paciente, pk=historia.paciente.id)

        self.request.session["pacienteListview_paciente_id"] = historia.paciente.id

        return initial
    
class HistoriaClinicaDetailView(DetailView):
    model = HistoriaClinica
    template_name = "core/historiaclinica_detail.html"
    context_object_name = "hc"

    def get_object(self):
        # Recuperar el `encoded_id` de los kwargs
        encoded_id = self.kwargs.get('encoded_id')
        
        # Decodificar el `encoded_id` usando base64
        try:
            decoded_id = decode_id(encoded_id)
        except (TypeError, ValueError):
            raise AttributeError("ID codificado no es válido.")
        
        # Buscar el objeto correspondiente
        return get_object_or_404(HistoriaClinica, pk=decoded_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Codificar el `id` del objeto actual usando base64
        encoded_id = encode_id(self.object.id)
        context['encoded_id'] = encoded_id  # Pasar el ID codificado al contexto

        context['form'] = HistoriaClinicaDetailForm(instance=self.object)

        #self.request.session["nro_hiscli"] = self.object.nro_hiscli
        self.request.session["pacienteListview_paciente_id"] = self.object.paciente.id

        return context

class SeleccionarServiciosView(FormView):
    template_name = 'core/seleccionar_servicios.html'
    form_class = SeleccionarServiciosForm

    def form_valid(self, form):
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(id=paciente_id)

        notas = form.cleaned_data['notas']
        fecha = form.cleaned_data['fecha']

        servicios = Servicios.objects.create(paciente=paciente, fecha=fecha,notas=notas)

        tipos_servicio = form.cleaned_data['tipos_servicio']
        for tipo_servicio in tipos_servicio:
            ServiciosDetalle.objects.create(servicio=servicios, tipo_servicio=tipo_servicio)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pacientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs['paciente_id']
        paciente = Paciente.objects.get(id=paciente_id)

        context['paciente'] = paciente

        self.request.session["pacienteListview_paciente_id"] = paciente_id

        return context
    
@login_required
def cita_consulta_medica(request):
    consulta_id = request.GET.get('id')
    consulta = get_object_or_404(ConsultaMedica, id=consulta_id)
    data = {
        'veterinario': consulta.medicoveterinario.nombres+' (CMVP'+consulta.medicoveterinario.numero_colegiatura+')',
        'motivo': consulta.motivo,
        'examen_fisico': consulta.examen_fisico,
        'diagnostico': consulta.diagnostico,
        'tratamiento': consulta.tratamiento,
        'notas_adicionales': consulta.notas_adicionales,
        'peso': consulta.peso,
        'fecha': consulta.fecha,
        # Agrega más campos si es necesario
    }
    return JsonResponse(data)

@login_required
def cita_servicio(request):
    servicio_id = request.GET.get('id')
    servicios = Servicios.objects.get(id=servicio_id)
    serviciosdetalle = ServiciosDetalle.objects.filter(servicio=servicios)

    data = {}
    contador = 1
    for servicio in serviciosdetalle:
        data[contador] = {'servicio':servicio.tipo_servicio.nombre}
        contador += 1
    
    data_response = {
        'data':data,
        'notas':servicios.notas,
        'fecha':servicios.fecha
    }

    return JsonResponse(data_response)

@login_required
def reescribir_paciente_id(request):

    paciente_id = request.GET.get('paciente_id')
    request.session['pacienteListview_paciente_id'] = paciente_id
    paciente = Paciente.objects.get(id = paciente_id)
    if paciente:
        return JsonResponse({'status': 'restaurado el id paciente','paciente_id':paciente.id})
    else:
        return JsonResponse({'status': 'id de paciente no hallado','paciente_id':None})

@login_required
def programar_cita(request,paciente_id):
    if request.method == 'POST':
        form = CitasProgramadasForm(request.POST)

        request.session["pacienteListview_paciente_id"] = paciente_id

        if form.is_valid():
            form.save()
            return redirect('pacientes')  # Redirige a una página de éxito
    else:
        # obtener los valores iniciales para el form
        paciente = get_object_or_404(Paciente, pk=paciente_id)
        contactopaciente_id = paciente.contactopaciente.id
        contactopaciente = get_object_or_404(ContactoPaciente, pk=contactopaciente_id)
        nombre_primario = contactopaciente.nombre_primario
        nombre_secundario = contactopaciente.nombre_secundario
        apellido_primario = contactopaciente.apellido_primario
        apellido_secundario = contactopaciente.apellido_secundario
        tipodocid = contactopaciente.tipodocid
        docum_identidad = contactopaciente.docum_identidad
        telef_movil = contactopaciente.telef_movil
        
        initial_data = {'paciente':paciente,'nombre_primario':nombre_primario,'nombre_secundario':nombre_secundario,
                        'apellido_primario':apellido_primario,'apellido_secundario':apellido_secundario,
                        'tipodocid':tipodocid,'docum_identidad':docum_identidad,'telef_movil':telef_movil}
        
        form = CitasProgramadasForm(initial=initial_data)

    def save(self, commit=True):
        instance = super().save(commit=False)

        paciente = get_object_or_404(Paciente, pk=paciente_id)
        contactopaciente_id = paciente.contactopaciente.id
        contactopaciente = get_object_or_404(ContactoPaciente, pk=contactopaciente_id)
        
        nombre_primario = contactopaciente.nombre_primario
        nombre_secundario = contactopaciente.nombre_secundario
        apellido_primario = contactopaciente.apellido_primario
        apellido_secundario = contactopaciente.apellido_secundario

        # Asignar el valor de cada campo
        
        instance.nombre_primario = nombre_primario
        instance.nombre_secundario = nombre_secundario
        instance.apellido_primario = apellido_primario
        instance.apellido_secundario = apellido_secundario

        if commit:
            instance.save()
        return instance

    return render(request, 'core/programar_cita.html', {'form': form})

@login_required
def programar_cita_nuevo_paciente(request):
    if request.method == 'POST':
        form = CitasProgramadasNuevoPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pacientes')  # Redirige a una página de éxito
    else:
        form = CitasProgramadasNuevoPacienteForm()
    return render(request, 'core/programar_cita_nuevo_paciente.html', {'form': form})


@login_required
def notificar_cita(request):
    ahora = datetime.now()

    # Rango de tiempo para notificaciones
    
    inicio_rango = (ahora + timedelta(minutes=30)).replace(second=0, microsecond=0)
    fin_rango = (ahora + timedelta(hours=1)).replace(second=0, microsecond=0)

    print('fecha actual',ahora.date(),'inicio rango hora',inicio_rango.time(),'fin rango hora',fin_rango.time())

    # Filtrar citas del día dentro del rango

    citas = CitasProgramadas.objects.filter(
        fecha_cita=ahora.date(),
        hora_cita__gte=inicio_rango.time(),
        hora_cita__lte=fin_rango.time()
    )

    for cita in citas:
        print(f"Cita: {cita.hora_cita}, Inicio Rango: {inicio_rango.time()}, Fin Rango: {fin_rango.time()}")

    # Formatear las citas como JSON
    citas_json = [
        {
            'paciente': f"{cita.paciente}",
            'telefono': f"{cita.telef_movil}",
            'nombre': f"{cita.nombre_primario} {cita.apellido_primario}",
            'hora': cita.hora_cita.strftime('%H:%M'),
            'notas': cita.notas,
        } for cita in citas
    ]

    return JsonResponse({'citas': citas_json})


@login_required
def vista_generar_historia_clinica(request, paciente_id):
    
    paciente = Paciente.objects.get(id=paciente_id)
    historiaclinica = HistoriaClinica.objects.get(paciente=paciente)
    empresacliente = EmpresaCliente.objects.all().first()
    sexo = ''
    if paciente.sexo == 'M':
        sexo = 'MACHO'
    else:
        sexo = 'HEMBRA'

    # Datos dinámicos para el PDF
    paciente_dicc = {
        "historia": historiaclinica.nro_hiscli,
        "fecha": historiaclinica.fecha,
        "nombre": paciente.nombre,
        "especie_raza": paciente.raza.especie.nombre +' - '+ paciente.raza.nombre,
        "color": paciente.color,
        "peso": paciente.peso,
        "edad": paciente.calcular_edad_detallada(),
        "chip": paciente.chip,
        "sexo": sexo,
        "ruta_imagen":os.path.join(settings.MEDIA_ROOT, paciente.imagen.name) if paciente.imagen else None,
    }

    if paciente.contactopaciente.tipo_contacto == 'D':
        tipocontacto = "Dueño"
    else:
        tipocontacto = "Responsable"

    contacto_paciente = {
        "nombres": paciente.contactopaciente.nombres,
        "direccion": paciente.contactopaciente.direccion,
        "email": paciente.contactopaciente.email,
        "docid": paciente.contactopaciente.docum_identidad,
        "tipo_contacto": tipocontacto,
        "tipo_docid": paciente.contactopaciente.tipodocid.desdocid,
        "telefonos": 'fijo '+paciente.contactopaciente.telef_fijo +' movil '+paciente.contactopaciente.telef_movil,
    }

    empresa_cliente = {
        "nombre":empresacliente.nombre,
        "ruc":empresacliente.ruc,
        "telefono":empresacliente.telefono,
        "email":empresacliente.email,
        "direccion":empresacliente.direccion,
        "ruta_logo":os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None,
    }

    historia_clinica = {
        "anamnesis": historiaclinica.anamnesis,
        "antecedentes_medicos": historiaclinica.antecedentes_medicos,
        "vacunas_aplicadas": historiaclinica.vacunas_aplicadas,
        "desparasitaciones": historiaclinica.desparasitaciones,
        "medicamentos_actuales": historiaclinica.medicamentos_actuales,
    }

    consultasmedicas = ConsultaMedica.objects.filter(paciente=paciente).order_by('fecha')
    consultasmedicas_lista = []
    for consulta in consultasmedicas:
        
        recetasmedica = RecetaMedica.objects.filter(consultamedica=consulta)
        posologia_lista = []
        for receta in recetasmedica:
            posologia_lista.append({'farmaco':receta.farmaco,'cantidad':receta.cantidad,'dosis':receta.dosis})

        consulta_medica = {
            'fecha': consulta.fecha,
            'veterinario':consulta.medicoveterinario.nombres+' (CMVP '+consulta.medicoveterinario.numero_colegiatura+')',
            'motivo':consulta.motivo,
            'examen_fisico': consulta.examen_fisico,
            'diagnostico':consulta.diagnostico,
            'tratamiento':consulta.tratamiento,
            'notas_adicionales':consulta.notas_adicionales,
            'posologia_lista':posologia_lista,
        }
        consultasmedicas_lista.append(consulta_medica)

    servicios = Servicios.objects.filter(paciente=paciente).order_by("fecha")

    servicios_lista = []

    for servicio in servicios:
        serviciosdetalle = ServiciosDetalle.objects.filter(servicio=servicio)
        servicios_cabecera = []
        servicio_detalle = {}
        for serviciodetalle in serviciosdetalle:
            servicio_detalle = {
                'categoria':serviciodetalle.tipo_servicio.categoria,
                'nombre':serviciodetalle.tipo_servicio.nombre,
            }
            servicios_cabecera.append(servicio_detalle)

        servicios_lista.append((servicio.fecha,servicio.notas,servicios_cabecera))

    #file_path = os.path.join("media", f"historia_clinica_{paciente_dicc['historia']}.pdf")
    ruta_media = os.path.join(settings.BASE_DIR,'media')
    file_path = os.path.join(ruta_media, f"historia_clinica_{paciente_dicc['historia']}.pdf")
    print("previo a generar",file_path)
    generar_historia_clinica(file_path, paciente_dicc, servicios, empresa_cliente,contacto_paciente,historia_clinica,consultasmedicas_lista,servicios_lista)

    try:
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="historia_clinica_{paciente_dicc["historia"]}.pdf"'
        return response
    finally:
        pass
        # Elimina el archivo una vez enviado
        #if os.path.exists(file_path):
        #    os.remove(file_path)

@login_required
def posologia_add(request,consultamedica_id):

    farmacos_registrados = request.session.get('posologia_add', [])

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':               
        
        farmaco = request.POST.get('farmaco')
        cantidad = request.POST.get('cantidad')
        dosis = request.POST.get('dosis')

        farmacos_registrados.append({'farmaco': farmaco, 'cantidad': cantidad,'dosis':dosis})

        request.session['posologia_add'] = farmacos_registrados

        return JsonResponse({'farmaco': farmaco, 'cantidad': cantidad,'dosis':dosis})

    if request.method == 'POST' and 'finalizar' in request.POST:

        farmacos_registrados = request.session.get('posologia_add', [])
        print("paso consulta medica",consultamedica_id)
        consultamedica = ConsultaMedica.objects.get(id=consultamedica_id)

        for farmaco_data in farmacos_registrados:
            print("paso 2")
            farmaco = farmaco_data['farmaco']
            cantidad = farmaco_data['cantidad']
            dosis = farmaco_data['dosis']
    
            RecetaMedica.objects.create(consultamedica=consultamedica,farmaco=farmaco,cantidad=cantidad,dosis=dosis)

        if 'posologia_add' in request.session:
            del request.session['posologia_add']

    return render(request, 'core/posologia_add.html', {'consultamedica_id': consultamedica_id, 'farmacos_registrados': farmacos_registrados})

@login_required
def posologia_limpia_lista_farmacos(request):
    if 'posologia_add' in request.session:
        del request.session['posologia_add']

@login_required
def pacientes_busqueda_relativa(request):
    if request.method == 'POST':
        nro_hiscli = request.POST.get('nro_hiscli','').strip()
        paciente_nombre = request.POST.get('paciente_nombre','').strip()
        contacto_nombres = request.POST.get('contacto_nombres','').strip()
        paginate_by = 12

        if nro_hiscli != "" and paciente_nombre == "" and contacto_nombres == "":
            paciente = Paciente.objects.filter(Q(historia__nro_hiscli__icontains=nro_hiscli)).first()

        if nro_hiscli == "" and paciente_nombre != "" and contacto_nombres == "":
            paciente = Paciente.objects.filter(Q(nombre__icontains=paciente_nombre)).first()

        if nro_hiscli == "" and paciente_nombre == "" and contacto_nombres != "":
            paciente = Paciente.objects.filter(Q(contactopaciente__nombres__icontains=contacto_nombres)).first()

        if nro_hiscli != "" and paciente_nombre != "" and contacto_nombres == "":
            paciente = Paciente.objects.filter(
                Q(historia__nro_hiscli__icontains=nro_hiscli) &  # Coincidencia parcial en nro_hiscli
                Q(nombre__icontains=paciente_nombre)  # Coincidencia parcial en paciente_nombre
            ).first()

        if nro_hiscli != "" and paciente_nombre == "" and contacto_nombres != "":
            paciente = Paciente.objects.filter(
                Q(historia__nro_hiscli__icontains=nro_hiscli) &  # Coincidencia parcial en nro_hiscli
                Q(contactopaciente__nombres__icontains=contacto_nombres)
            ).first()

        if nro_hiscli == "" and paciente_nombre != "" and contacto_nombres != "":
            paciente = Paciente.objects.filter(
                Q(contactopaciente__nombres__icontains=contacto_nombres) &  # Coincidencia parcial en contacto_nombres
                Q(nombre__icontains=paciente_nombre)  # Coincidencia parcial en paciente_nombre
            ).first()

        if nro_hiscli != "" and paciente_nombre != "" and contacto_nombres != "":
            paciente = Paciente.objects.filter(
                Q(historia__nro_hiscli__icontains=nro_hiscli) &  # Coincidencia parcial en nro_hiscli
                Q(contactopaciente__nombres__icontains=contacto_nombres) &  # Coincidencia parcial en contacto_nombres
                Q(nombre__icontains=paciente_nombre)  # Coincidencia parcial en paciente_nombre
            ).first()

        page_number = 0

        if not paciente:
            return JsonResponse({'page_number': page_number,'paciente_encontrado':None})

        #print("paciente ",paciente.nombre," ",paciente.id)
        #print("paciente",paciente_nombre,"contacto",contacto_nombres,"historia",nro_hiscli)

        #print("segun busqueda paciente",paciente.nombre,"contacto",paciente.contactopaciente.nombres,"historia",paciente.historia.nro_hiscli)

        # Obtener el contacto relacionado con el paciente
        contacto_nombre = paciente.contactopaciente.nombres
        
        # Obtener pacientes que cumplen el orden lógico deseado
        pacientes_filtrados = Paciente.objects.filter(
            Q(nombre__lt=paciente.nombre) |  # Pacientes con nombre menor (alfabéticamente)
            Q(nombre=paciente.nombre, contactopaciente__nombres__lte=contacto_nombre)  # Pacientes con el mismo nombre pero contacto menor o igual
        ).order_by('nombre', 'contactopaciente__nombres')

        # Contar la cantidad total de pacientes
        contador_pacientes = pacientes_filtrados.count()
                        
        # Calcular el número de página correspondiente
        page_number = 1

        if (contador_pacientes) > paginate_by and ((contador_pacientes) % paginate_by) != 0: 
            page_number = (contador_pacientes) // paginate_by + 1 
        elif (contador_pacientes) > paginate_by and ((contador_pacientes) % paginate_by) == 0:
            page_number = (contador_pacientes) // paginate_by

        #print("page_number",page_number)

        return JsonResponse({'page_number': page_number,'paciente_encontrado': paciente.nombre,'paciente_id':paciente.id})

class MedicoVeterinarioListView(ListView):
    model = MedicoVeterinario
    paginate_by = 12  # Número de elementos por página

class MedicoVeterinarioCreate(CreateView):
    model = MedicoVeterinario
    form_class = MedicoVeterinarioForm
    success_url = reverse_lazy('medicoveterinario_create')

class MedicoVeterinarioUpdate(UpdateView):
    model = MedicoVeterinario
    form_class = MedicoVeterinarioForm
    template_name_suffix = "_update_form"
 
    def get_success_url(self):
        return reverse_lazy('medicoveterinario_update', args=[self.object.id]) + "?ok"

class MedicoVeterinarioDelete(DeleteView):
    model = MedicoVeterinario
    success_url = reverse_lazy("medicoveterinario_list")

class TipoServicioListView(ListView):
    model = TipoServicio
    paginate_by = 24  # Número de elementos por página
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        tiposervicios = context['object_list']
        for tiposervicio in tiposervicios:
            print("tipo servicio",tiposervicio,tiposervicio.categoria)
            if tiposervicio.categoria == "S":
                tiposervicio.destipo = "Servicios complementarios"
            else:
                tiposervicio.destipo = "Clinicos"
        
        context["destipo"] = tiposervicios
        print(context)
        return  context

class TipoServicioCreate(CreateView):
    model = TipoServicio
    form_class = TipoServicioForm
    success_url = reverse_lazy('tiposervicio_create')

class TipoServicioUpdate(UpdateView):
    model = TipoServicio
    form_class = TipoServicioForm
    template_name_suffix = "_update_form"
 
    def get_success_url(self):
        return reverse_lazy('tiposervicio_update', args=[self.object.id]) + "?ok"

class TipoServicioDelete(DeleteView):
    model = TipoServicio
    success_url = reverse_lazy("tiposervicio_list")

class EspecieListView(ListView):
    model = Especie
    paginate_by = 24  # Número de elementos por página

class EspecieCreate(CreateView):
    model = Especie
    form_class = EspecieForm
    success_url = reverse_lazy('especie_create')

class EspecieUpdate(UpdateView):
    model = Especie
    form_class = EspecieForm
    template_name_suffix = "_update_form"
 
    def get_success_url(self):
        return reverse_lazy('especie_update', args=[self.object.id]) + "?ok"

class EspecieDelete(DeleteView):
    model = Especie
    success_url = reverse_lazy("especie_list")

class RazaListView(ListView):
    model = Raza
    paginate_by = 24  # Número de elementos por página


class RazaCreate(CreateView):
    model = Raza
    form_class = RazaForm
    success_url = reverse_lazy('raza_create')

class RazaUpdate(UpdateView):
    model = Raza
    form_class = RazaForm
    template_name_suffix = "_update_form"
 
    def get_success_url(self):
        return reverse_lazy('raza_update', args=[self.object.id]) + "?ok"

class RazaDelete(DeleteView):
    model = Raza
    success_url = reverse_lazy("raza_list")

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige a la página de inicio después de cerrar sesión

def exportaPDF_especies(request):
    # Renderiza la plantilla HTML con el contexto proporcionado
    especies = Especie.objects.all()
    empresacliente = EmpresaCliente.objects.all().first()
    ruta_logo = os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None
    print(ruta_logo)

    # Convertir la imagen a base64
    if ruta_logo:
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_string = None

    html_string = render_to_string('core/especie_list_pdf.html',{'especies': especies,'ruta_logo_base64':encoded_string}, request=request )

    # Convierte la cadena HTML en un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=especies.pdf'

    # Construir URLs absolutas para los recursos estáticos
    html_string = html_string.replace('href="/static/', 'href="' + request.build_absolute_uri('/static/'))

    HTML(string=html_string).write_pdf(response)

    return response

def exportaPDF_razas(request):
    # Renderiza la plantilla HTML con el contexto proporcionado
    razas = Raza.objects.all()
    empresacliente = EmpresaCliente.objects.all().first()
    ruta_logo = os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None
    print(ruta_logo)

    # Convertir la imagen a base64
    if ruta_logo:
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_string = None

    html_string = render_to_string('core/raza_list_pdf.html',{'razas': razas,'ruta_logo_base64':encoded_string,'ruta_logo':ruta_logo}, request=request )

    # Convierte la cadena HTML en un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=razas.pdf'

    # Construir URLs absolutas para los recursos estáticos
    html_string = html_string.replace('href="/static/', 'href="' + request.build_absolute_uri('/static/'))

    HTML(string=html_string).write_pdf(response)

    return response

def exportaPDF_tiposervicios(request):
    # Renderiza la plantilla HTML con el contexto proporcionado
    tiposervicio = TipoServicio.objects.all()
    empresacliente = EmpresaCliente.objects.all().first()
    ruta_logo = os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None
    print(ruta_logo)

    # Convertir la imagen a base64
    if ruta_logo:
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_string = None

    html_string = render_to_string('core/tiposervicio_list_pdf.html',{'tiposervicio': tiposervicio,'ruta_logo_base64':encoded_string,'ruta_logo':ruta_logo}, request=request )

    # Convierte la cadena HTML en un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=tiposervicio.pdf'

    # Construir URLs absolutas para los recursos estáticos
    html_string = html_string.replace('href="/static/', 'href="' + request.build_absolute_uri('/static/'))

    HTML(string=html_string).write_pdf(response)

    return response

def exportaPDF_medicoveterinario(request):
    # Renderiza la plantilla HTML con el contexto proporcionado
    medicoveterinario = MedicoVeterinario.objects.all()
    empresacliente = EmpresaCliente.objects.all().first()
    ruta_logo = os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None
    print(ruta_logo)

    # Convertir la imagen a base64
    if ruta_logo:
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_string = None

    html_string = render_to_string('core/medicoveterinario_list_pdf.html',{'medicoveterinario': medicoveterinario,'ruta_logo_base64':encoded_string,'ruta_logo':ruta_logo}, request=request )

    # Convierte la cadena HTML en un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=medicoveterinario.pdf'

    # Construir URLs absolutas para los recursos estáticos
    html_string = html_string.replace('href="/static/', 'href="' + request.build_absolute_uri('/static/'))

    HTML(string=html_string).write_pdf(response)

    return response

def exportaPDF_pacientes(request):
    # Renderiza la plantilla HTML con el contexto proporcionado
    paciente = Paciente.objects.all()
    empresacliente = EmpresaCliente.objects.all().first()
    ruta_logo = os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None
    print(ruta_logo)

    # Convertir la imagen a base64
    if ruta_logo:
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_string = None

    html_string = render_to_string('core/paciente_list_pdf.html',{'pacientes': paciente,'ruta_logo_base64':encoded_string,'ruta_logo':ruta_logo}, request=request )

    # Convierte la cadena HTML en un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=paciente.pdf'

    # Construir URLs absolutas para los recursos estáticos
    html_string = html_string.replace('href="/static/', 'href="' + request.build_absolute_uri('/static/'))

    HTML(string=html_string).write_pdf(response)

    return response

class CitasProgramadasListView(ListView):
    model = CitasProgramadas
    paginate_by = 24  # Número de elementos por página

from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'

class PacienteDelete(DeleteView):
    model = Paciente
    success_url = reverse_lazy("pacientes")

class ContactoPacienteDelete(DeleteView):
    model = ContactoPaciente
    success_url = reverse_lazy("pacientes")

class HistoriaClinicaDelete(DeleteView):
    model = HistoriaClinica
    success_url = reverse_lazy("pacientes")

class ServiciosListView(ListView):
    model = Servicios
    paginate_by = 24  # Número de elementos por página
    def get_queryset(self): 
        queryset = super().get_queryset()
        #servicio = Servicios.objects.filter(id=self.id)
        for servicio in queryset: 
            nombre_servicio = "\n".join([str(serviciodetalle.tipo_servicio.nombre) for serviciodetalle in ServiciosDetalle.objects.filter(servicio=servicio)])
            servicio.concatenado = nombre_servicio
            servicioxpaciente = Servicios.objects.get(id=servicio.id)
            nro_hiscli = servicioxpaciente.paciente.historia.nro_hiscli
            servicio.nro_hiscli = nro_hiscli

        return queryset

class ServiciosDelete(DeleteView):
    model = Servicios
    success_url = reverse_lazy("servicios_list")

class ConsultaMedicaListView(ListView):
    model = ConsultaMedica
    paginate_by = 24  # Número de elementos por página

class ConsultaMedicaDelete(DeleteView):
    model = ConsultaMedica
    success_url = reverse_lazy("consulta_medica_list")

def exportaPDF_servicios(request):
    # Renderiza la plantilla HTML con el contexto proporcionado
    servicios = Servicios.objects.all()

    for servicio in servicios:
        nombre_servicio = "\n".join([str(serviciodetalle.tipo_servicio.nombre) for serviciodetalle in ServiciosDetalle.objects.filter(servicio=servicio)])
        servicio.concatenado = nombre_servicio

    empresacliente = EmpresaCliente.objects.all().first()
    ruta_logo = os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None

    # Convertir la imagen a base64
    if ruta_logo:
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_string = None

    html_string = render_to_string('core/servicios_list_pdf.html',{'servicios': servicios,'ruta_logo_base64':encoded_string,'ruta_logo':ruta_logo}, request=request )

    # Convierte la cadena HTML en un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=servicios.pdf'

    # Construir URLs absolutas para los recursos estáticos
    html_string = html_string.replace('href="/static/', 'href="' + request.build_absolute_uri('/static/'))

    HTML(string=html_string).write_pdf(response)

    return response

def exportaPDF_consultamedica(request):
    # Renderiza la plantilla HTML con el contexto proporcionado
    consultasmedicas = ConsultaMedica.objects.all()

    empresacliente = EmpresaCliente.objects.all().first()
    ruta_logo = os.path.join(settings.MEDIA_ROOT, empresacliente.logo.name) if empresacliente.logo else None

    # Convertir la imagen a base64
    if ruta_logo:
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_string = None

    html_string = render_to_string('core/consultasmedicas_list_pdf.html',{'consultasmedicas': consultasmedicas,'ruta_logo_base64':encoded_string,'ruta_logo':ruta_logo}, request=request )

    # Convierte la cadena HTML en un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=consultasmedicas.pdf'

    # Construir URLs absolutas para los recursos estáticos
    html_string = html_string.replace('href="/static/', 'href="' + request.build_absolute_uri('/static/'))

    HTML(string=html_string).write_pdf(response)

    return response
