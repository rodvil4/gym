from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre", max_length=60, blank=False, null=False)
    ap_pat = models.CharField("Apellido Paterno", max_length=60, blank=False, null=False)
    ap_mat = models.CharField("Apellido Materno", max_length=60)
    GENERO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]
    genero = models.CharField("Género", max_length=1, choices=GENERO_CHOICES, blank=False, null=False)
    fec_nac = models.DateField("Fecha de Nacimiento", blank=False, null=False)
    telefono = models.CharField("Teléfono", max_length=12, blank=False, null=False)
    email = models.EmailField("Correo Electrónico", unique=True, blank=False, null=False)
    direccion = models.CharField("Direccion", max_length=250)
    fec_reg = models.DateTimeField("Fecha de Registro", default=timezone.now, blank=False, null=False)
    estatus = models.BooleanField("Estatus", default=True, blank=False, null=False)

    def __str__(self):
        return f"{self.nombre} {self.ap_pat}"

class Instructor(models.Model):
    nombre = models.CharField("Nombre Completo", max_length=120, blank=False,  null=False)
    fec_nac = models.DateField("Fecha de Nacimiento", blank=False, null=False)
    telefono = models.CharField("Teléfono", max_length=12, blank=False, null=False)
    estudios = models.CharField("Estudios", max_length=100, blank=True, null=True)
    certificacion = models.CharField("Estudios", max_length=100, blank=True, null=True)
    GENERO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]
    genero = models.CharField("Género", max_length=1, choices=GENERO_CHOICES, blank=False, null=False)
    email = models.EmailField("Correo Electrónico", blank=False, null=False)
    direccion = models.CharField("Direccion", max_length=250)
    fec_reg = models.DateTimeField("Fecha de Registro", default=timezone.now, blank=False, null=False)
    estatus = models.BooleanField("Estatus", default=True, blank=False, null=False)
    def __str__(self):
        return f"{self.nombre} "

class Tclass(models.Model):
    describe = models.CharField("Curso ", max_length=80,blank=False, null=False)
    duracion = models.IntegerField("Tiempo(min)")
    requisitos = models.CharField("Requisitos",max_length=120, blank=True, null=True)
    observa = models.CharField("Observaciones",max_length=300, blank=True, null=False)
    minimo = models.IntegerField("Minimo integrantes", default=1)
    maximo = models.IntegerField("Maximo integrantes", default=10)
    fec_reg = models.DateTimeField("Fecha de Registro", default=timezone.now, blank=False, null=False)
    estatus = models.BooleanField("Estatus", default=True, blank=False, null=False)
    creo = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.describe} "

class Grupo(models.Model):
    grupo = models.CharField("Grupo", max_length=80, blank=False, null=False)
    clase = models.ForeignKey(Tclass, on_delete=models.CASCADE, blank=False, null=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    observa = models.CharField("Observaciones",max_length=300, blank=True, null=False)
    MODALIDAD_CHOICES = [
        ('P', 'Presencial'),
        ('R', 'Remoto'),
        ('H', 'Hibrido'),
    ]
    modalidad = models.CharField("Modalidad", max_length=1, choices=MODALIDAD_CHOICES, blank=False, null=False)
    costo = models.DecimalField("Costo Curso",
        max_digits=9,  # 7 enteros + 2 decimales = 9 dígitos en total
        decimal_places=2,  # Especifica 2 decimales
        default=1.00  # Valor por defecto (opcional)
    )
    preciounitario = models.DecimalField("Precio x Persona",
        max_digits=9,  # 7 enteros + 2 decimales = 9 dígitos en total
        decimal_places=2,  # Especifica 2 decimales
        default=1.00  # Valor por defecto (opcional)
    )
    minimo = models.IntegerField("Minimo integrantes", default=1)
    maximo = models.IntegerField("Maximo integrantes", default=10)
    duracion = models.IntegerField("Tiempo(min)")
    horaInicio = models.TimeField("Hora Inicial")  # Utiliza TimeField para almacenar la hora
    horaTermino = models.TimeField("Hora Termina")  # Utiliza TimeField para almacenar la hora

    fec_reg = models.DateTimeField("Fecha de Registro", default=timezone.now, blank=False, null=False)
    estatus = models.BooleanField("Estatus", default=True, blank=False, null=False)
    creo = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    dias_semana = models.JSONField("Días de la semana", default=dict, blank=False, null=False )

    def __str__(self):
        return f"{self.grupo} - {self.instructor}"


