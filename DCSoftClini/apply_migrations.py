import os
import sys
import django
from django.core.management import call_command

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '_internal'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_internal.DCSoftClini.settings')

django.setup()
call_command('makemigrations')
call_command('migrate')
