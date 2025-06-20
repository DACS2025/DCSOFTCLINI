# Generated by Django 5.1.7 on 2025-05-07 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_paciente_fecha'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='citasprogramadas',
            options={'ordering': ['-fecha_cita', '-hora_cita']},
        ),
        migrations.AlterModelOptions(
            name='servicios',
            options={'ordering': ['paciente']},
        ),
        migrations.AlterField(
            model_name='recetamedica',
            name='consultamedica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.consultamedica', verbose_name='Consulta Medica'),
        ),
    ]
