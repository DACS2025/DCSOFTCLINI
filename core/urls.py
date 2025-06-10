from django.urls import path
from . import views
from .views import historia_clinica,home,PacienteListView,PacienteCreateView,ContactoPacienteCreateView,HistoriaClinicaCreateView,ConsultaMedicaCreateView,HistoriaClinicaDetailView,SeleccionarServiciosView,cita_consulta_medica, cita_servicio,reescribir_paciente_id,programar_cita,programar_cita_nuevo_paciente,notificar_cita,vista_generar_historia_clinica,posologia_add,posologia_limpia_lista_farmacos,pacientes_busqueda_relativa,MedicoVeterinarioListView, MedicoVeterinarioCreate, MedicoVeterinarioDelete,MedicoVeterinarioUpdate,TipoServicioListView,TipoServicioCreate,TipoServicioUpdate,TipoServicioDelete,EspecieListView,EspecieCreate,EspecieUpdate,EspecieDelete,RazaListView,RazaCreate,RazaUpdate,RazaDelete,PacienteUpdate,ContactoPacienteUpdate,HistoriaClinicaUpdate,PacienteDelete,ContactoPacienteDelete,HistoriaClinicaDelete,logout_view,exportaPDF_especies, exportaPDF_razas, exportaPDF_tiposervicios, exportaPDF_servicios, exportaPDF_medicoveterinario,exportaPDF_pacientes,CitasProgramadasListView,CustomPasswordChangeDoneView,CustomPasswordChangeView,ServiciosListView, ServiciosDelete, ConsultaMedicaListView, ConsultaMedicaDelete, exportaPDF_consultamedica
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', home, name='home'),
    path('dcclini/historias/', historia_clinica, name='historias'),
    path('dcclini/historias/detail/<str:encoded_id>/',login_required(HistoriaClinicaDetailView.as_view()), name='historiaclinica_detail'),
    path('dcclini/pacientes/', login_required(PacienteListView.as_view()), name='pacientes'),
    path('dcclini/pacientes/<str:nro_hiscli>/', login_required(PacienteListView.as_view()), name='pacientes_nro_hiscli'),
    path('dcclini/pacientes/add/<int:contactopaciente_id>/',login_required(PacienteCreateView.as_view()), name='paciente_add'),
    path('dcclini/pacientes/add/<int:contactopaciente_id>/',login_required(PacienteCreateView.as_view()), name='paciente_add_id'),
    path('dcclini/pacientes/update/<int:pk>/',login_required(PacienteUpdate.as_view()), name='paciente_update'),
    path('dcclini/pacientes/delete/<int:pk>/',login_required(PacienteDelete.as_view()), name='paciente_delete'),

    path('dcclini/servicios/list/', login_required(ServiciosListView.as_view()), name='servicios_list'),

    path('dcclini/medicos/', login_required(MedicoVeterinarioListView.as_view()), name='medicoveterinario_list'),
    path('dcclini/medico/update/<int:pk>/', login_required(MedicoVeterinarioUpdate.as_view()), name='medicoveterinario_update'),
    path('dcclini/medico/delete/<int:pk>/', login_required(MedicoVeterinarioDelete.as_view()), name='medicoveterinario_delete'),
    path('dcclini/medico/create/', login_required(MedicoVeterinarioCreate.as_view()), name='medicoveterinario_create'),

    path('dcclini/tiposervicios/', login_required(TipoServicioListView.as_view()), name='tiposervicio_list'),
    path('dcclini/tiposervicio/update/<int:pk>/', login_required(TipoServicioUpdate.as_view()), name='tiposervicio_update'),
    path('dcclini/tiposervicio/delete/<int:pk>/', login_required(TipoServicioDelete.as_view()), name='tiposervicio_delete'),
    path('dcclini/tiposervicio/create/', login_required(TipoServicioCreate.as_view()), name='tiposervicio_create'),

    path('dcclini/especies/', login_required(EspecieListView.as_view()), name='especie_list'),
    path('dcclini/especie/update/<int:pk>/', login_required(EspecieUpdate.as_view()), name='especie_update'),
    path('dcclini/especie/delete/<int:pk>/', login_required(EspecieDelete.as_view()), name='especie_delete'),
    path('dcclini/especie/create/', login_required(EspecieCreate.as_view()), name='especie_create'),

    path('dcclini/razas/', login_required(RazaListView.as_view()), name='raza_list'),
    path('dcclini/raza/update/<int:pk>/', login_required(RazaUpdate.as_view()), name='raza_update'),
    path('dcclini/raza/delete/<int:pk>/', login_required(RazaDelete.as_view()), name='raza_delete'),
    path('dcclini/raza/create/', login_required(RazaCreate.as_view()), name='raza_create'),

    path('dcclini/contactopacientes/add/',login_required(ContactoPacienteCreateView.as_view()), name='contactopaciente_add'),
    path('dcclini/contactopacientes/update/<int:pk>/<int:paciente_id>/',login_required(ContactoPacienteUpdate.as_view()), name='contactopaciente_update'),

    path('dcclini/contactopacientes/delete/<int:pk>/<int:paciente_id>/',login_required(ContactoPacienteDelete.as_view()), name='contactopaciente_delete'),

    path('dcclini/historia/add/detail/<str:encoded_id>/',login_required(HistoriaClinicaCreateView.as_view()), name='historia_add'),
    path('dcclini/historia/update/<int:pk>/',login_required(HistoriaClinicaUpdate.as_view()), name='historia_update'),
    path('dcclini/historia/delete/<int:pk>/',login_required(HistoriaClinicaDelete.as_view()), name='historia_delete'),

    path('dcclini/consultamedica/add/<str:nro_hiscli>/',login_required(ConsultaMedicaCreateView.as_view()), name='consulta_medica'),
    path('dcclini/servicios/detail/<int:paciente_id>/', login_required(SeleccionarServiciosView.as_view()), name='servicios'),
    path('dcclini/citas/consulta/', cita_consulta_medica, name='cita_consulta_medica'),
    path('dcclini/citas/servicio/', cita_servicio, name='cita_servicio'),
    path('reescribir_paciente_id/', reescribir_paciente_id, name='reescribir_paciente_id'),
    path('dcclini/programar_cita/<int:paciente_id>/', programar_cita, name='programar_cita'),
    path('dcclini/programar_cita_nuevo_paciente/', programar_cita_nuevo_paciente, name='programar_cita_nuevo_paciente'),
    path('dcclini/notificar_cita/', notificar_cita, name='notificar_cita'),
    path('dcclini/historia_clinica_pdf/<int:paciente_id>/', vista_generar_historia_clinica, name='generar_historia_clinica_pdf'),
    path('dcclini/posologia_add/<int:consultamedica_id>/', posologia_add, name='posologia_add'),
    path('dcclini/posologia_limpia_lista_farmacos/', posologia_limpia_lista_farmacos, name='posologia_limpia_lista_farmacos'),
    path('dcclini/pacientes_busqueda_relativa/', pacientes_busqueda_relativa, name='pacientes_busqueda_relativa'),
    path('dcclini/logout/', logout_view, name='logout'),

    path('dcclini/exportaPDF_especies/',exportaPDF_especies,name='exportaPDF_especies'),
    path('dcclini/exportaPDF_razas/',exportaPDF_razas,name='exportaPDF_razas'),
    path('dcclini/exportaPDF_tiposervicios/',exportaPDF_tiposervicios,name='exportaPDF_tiposervicios'),
    path('dcclini/exportaPDF_servicios/',exportaPDF_servicios,name='exportaPDF_servicios'),
    path('dcclini/exportaPDF_consultamedica/',exportaPDF_consultamedica,name='exportaPDF_consultamedica'),
    path('dcclini/exportaPDF_medicoveterinario/',exportaPDF_medicoveterinario,name='exportaPDF_medicoveterinario'),
    path('dcclini/exportaPDF_pacientes/',exportaPDF_pacientes,name='exportaPDF_pacientes'),

    path('dcclini/citas_programadas/', login_required(CitasProgramadasListView.as_view()), name='citas_programadas'),
    path('accounts/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('dcclini/servicios/delete/<int:pk>/', login_required(ServiciosDelete.as_view()), name='servicio_delete'),
    path('dcclini/consultamedica/list/',login_required(ConsultaMedicaListView.as_view()), name='consulta_medica_list'),
    path('dcclini/consultamedica/delete/<int:pk>/', login_required(ConsultaMedicaDelete.as_view()), name='consulta_medica_delete'),

]

