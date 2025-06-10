import base64

from .models import HistoriaClinica, Paciente

def encode_id(pk):
    return base64.urlsafe_b64encode(str(pk).encode()).decode()

def decode_id(encoded_pk):
    return int(base64.urlsafe_b64decode(encoded_pk).decode())
