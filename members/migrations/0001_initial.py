# Generated by Django 5.1.5 on 2025-02-12 00:54

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre Completo')),
                ('fec_nac', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('telefono', models.CharField(max_length=12, verbose_name='Teléfono')),
                ('estudios', models.CharField(blank=True, max_length=100, null=True, verbose_name='Estudios')),
                ('certificacion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Estudios')),
                ('genero', models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer')], max_length=1, verbose_name='Género')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('direccion', models.CharField(max_length=250, verbose_name='Direccion')),
                ('fec_reg', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Registro')),
                ('estatus', models.BooleanField(default=True, verbose_name='Estatus')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre')),
                ('ap_pat', models.CharField(max_length=60, verbose_name='Apellido Paterno')),
                ('ap_mat', models.CharField(max_length=60, verbose_name='Apellido Materno')),
                ('genero', models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer')], max_length=1, verbose_name='Género')),
                ('fec_nac', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('telefono', models.CharField(max_length=12, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('direccion', models.CharField(max_length=250, verbose_name='Direccion')),
                ('fec_reg', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Registro')),
                ('estatus', models.BooleanField(default=True, verbose_name='Estatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('describe', models.CharField(max_length=80, verbose_name='Curso ')),
                ('duracion', models.IntegerField(verbose_name='Tiempo(min)')),
                ('requisitos', models.CharField(blank=True, max_length=120, null=True, verbose_name='Requisitos')),
                ('observa', models.CharField(blank=True, max_length=300, verbose_name='Observaciones')),
                ('minimo', models.IntegerField(default=1, verbose_name='Minimo integrantes')),
                ('maximo', models.IntegerField(default=10, verbose_name='Maximo integrantes')),
                ('fec_reg', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Registro')),
                ('estatus', models.BooleanField(default=True, verbose_name='Estatus')),
                ('creo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(max_length=80, verbose_name='Grupo')),
                ('observa', models.CharField(blank=True, max_length=300, verbose_name='Observaciones')),
                ('modalidad', models.CharField(choices=[('P', 'Presencial'), ('R', 'Remoto'), ('H', 'Hibrido')], max_length=1, verbose_name='Modalidad')),
                ('costo', models.DecimalField(decimal_places=2, default=1.0, max_digits=9, verbose_name='Costo Curso')),
                ('preciounitario', models.DecimalField(decimal_places=2, default=1.0, max_digits=9, verbose_name='Precio x Persona')),
                ('minimo', models.IntegerField(default=1, verbose_name='Minimo integrantes')),
                ('maximo', models.IntegerField(default=10, verbose_name='Maximo integrantes')),
                ('duracion', models.IntegerField(verbose_name='Tiempo(min)')),
                ('horaInicio', models.TimeField(verbose_name='Hora Inicial')),
                ('horaTermino', models.TimeField(verbose_name='Hora Termina')),
                ('fec_reg', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Registro')),
                ('estatus', models.BooleanField(default=True, verbose_name='Estatus')),
                ('dias_semana', models.JSONField(default=dict, verbose_name='Días de la semana')),
                ('creo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.instructor')),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.tclass')),
            ],
        ),
    ]
