from datetime import datetime, timedelta
from .models import CitasProgramadas,Parametros_sist

def citas_hoy(request):
    ahora = datetime.now()

    # Rango de tiempo para notificaciones
    inicio_rango = (ahora + timedelta(minutes=30)).replace(second=0, microsecond=0)
    fin_rango = (ahora + timedelta(hours=1)).replace(second=0, microsecond=0)

    # Filtrar citas de hoy que coincidan con el rango de tiempo
    citas = CitasProgramadas.objects.filter(
        fecha_cita=ahora.date(),  # Citas del día actual
        hora_cita__gte=inicio_rango.time(),
        hora_cita__lte=fin_rango.time()
    )

    return {'citas_hoy': citas}

def frecuencia_notificacion_cita(request):
    parametro = Parametros_sist.objects.first()
    return {'frecuencia_notificacion_cita': parametro.frecuencia_notificacion_cita if parametro else 30000}
