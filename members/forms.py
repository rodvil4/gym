from django import forms
from .models import Member, Instructor, Tclass, Grupo
from django.core.validators import MinValueValidator, MaxValueValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from datetime import date 
from django.core.exceptions import ValidationError

class MemberRegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['nombre', 'ap_pat', 'ap_mat', 'genero', 'fec_nac', 'telefono', 'email', 'direccion', 'estatus']
        widgets = {
            'fec_nac': forms.DateInput(attrs={'type': 'date'}),
            'telefono': forms.TextInput(attrs={'pattern': '[0-9]{2}-[0-9]{4}-[0-9]{4}', 'placeholder': '99-9999-9999'}),
            'direccion': forms.Textarea(attrs={'rows': 4, 'cols': 70}),
        }

    def clean_email(self):
        """Validar que el email sea único excepto en la edición del mismo registro"""
        email = self.cleaned_data.get('email')
        instance = self.instance  # Obtener la instancia actual (si existe)

        # Filtrar por email, excluyendo el registro actual si es una edición
        if Member.objects.filter(email=email).exclude(pk=instance.pk).exists():
            raise ValidationError("Este correo electrónico ya está registrado en otro usuario. Usa otro diferente.")
        
        return email

    def clean_fec_nac(self):
        """Validar que la fecha de nacimiento corresponda a una persona mayor de 18 años"""
        fec_nac = self.cleaned_data.get('fec_nac')
        today = date.today()
        age = today.year - fec_nac.year - ((today.month, today.day) < (fec_nac.month, fec_nac.day))

        if age < 18:
            raise ValidationError("Debes tener al menos 18 años para registrarte.")
        
        return fec_nac

    def __init__(self, *args, **kwargs):
        super(MemberRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Row( Column('nombre', css_class='form-group col-md-4 mb-0'),
                     Column('ap_pat', css_class='form-group col-md-4 mb-0'),
                     Column('ap_mat', css_class='form-group col-md-4 mb-0'),
                     css_class='form-row'                 ),
                Row( Column('genero', css_class='form-group col-md-12 mb-0'),                 ),
                Row( Column('fec_nac', css_class='form-group col-md-12 mb-0'),                 ),
                Row( Column('telefono', css_class='form-group col-md-12 mb-0'),                ),
                Row( Column('email', css_class='form-group col-md-12 mb-0'),                ),
                Row( Column('direccion', css_class='form-group col-md-12 mb-0'),                ),
                Row( Column('estatus', css_class='form-group col-md-12 mb-0'),                ),
                css_class='container'
            )
        )


class MiFormulario(forms.Form):
    telefono = forms.CharField(max_length=12, 
                               widget=forms.TextInput(attrs={'id': 'telefono'}))

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['nombre', 'fec_nac', 'telefono', 'estudios', 'certificacion', 'genero', 'email', 'direccion','estatus']
        widgets = {
            'fec_nac': forms.DateInput(attrs={'type': 'date'}),
            'telefono': forms.TextInput(attrs={'pattern': '[0-9]{2}-[0-9]{4}-[0-9]{4}', 'placeholder': '99-9999-9999'}),
            'direccion': forms.Textarea(attrs={'rows': 2, 'cols': 70}),        
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Tclass
        fields = ['describe', 'duracion', 'requisitos', 'observa', 'minimo', 'maximo', 'estatus']
        widgets = {
            'observa': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
        }

    duracion = forms.IntegerField(
        validators=[
            MinValueValidator(10, message="Minimo debe durar 10 minutos"),
            MaxValueValidator(300, message="Maximo debe durar 300 minutos"),
        ] )
    minimo = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Participantes minimo 1"),
            MaxValueValidator(50, message="Participantes minimo maximo 50"),
        ] )
    maximo = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Participantes maximo minimo 50"),
            MaxValueValidator(300, message="Maximo de participantes 300"),
        ] )
    def clean(self):
        cleaned_data = super().clean()
        minimo_value = cleaned_data.get('minimo')
        maximo_value = cleaned_data.get('maximo')

        if minimo_value is not None and maximo_value is not None:
            if maximo_value < minimo_value:
                raise forms.ValidationError(
                    "El valor máximo debe ser mayor o igual al valor mínimo."
                )

        return cleaned_data


class GroupForm(forms.ModelForm):
    DIAS_SEMANA_CHOICES = [
        ('DO', 'Domingo'),
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miércoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sábado'),
    ]    
    dias_semana = forms.MultipleChoiceField(
        choices=DIAS_SEMANA_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'dias-semana-checkbox'}),
        label="Días de la semana",
        required=False
    )
    class Meta:
        model = Grupo
        fields = ['grupo','clase','instructor','observa','modalidad','costo','preciounitario','minimo','maximo','duracion','horaInicio','horaTermino','estatus','dias_semana']
        widgets = {
            'observa': forms.Textarea(attrs={'rows': 2, 'cols': 90}),
        }
    duracion = forms.IntegerField(
        validators=[
            MinValueValidator(10, message="Minimo debe durar 10 minutos"),
            MaxValueValidator(300, message="Maximo debe durar 300 minutos"),
        ] )
    minimo = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Participantes minimo 1"),
            MaxValueValidator(50, message="Participantes minimo maximo 50"),
        ] )
    maximo = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Participantes maximo minimo 50"),
            MaxValueValidator(300, message="Maximo de participantes 300"),
        ] )
    def clean(self):
        cleaned_data = super().clean()
        minimo_value = cleaned_data.get('minimo')
        maximo_value = cleaned_data.get('maximo')
        costo_value = cleaned_data.get('costo')
        precio_value = cleaned_data.get('preciounitario')

        if minimo_value is not None and maximo_value is not None:
            if maximo_value < minimo_value:
                raise forms.ValidationError(
                    "El valor máximo debe ser mayor o igual al valor mínimo."
                )

        if costo_value is not None and maximo_value is not None:
            if precio_value < costo_value:
                raise forms.ValidationError('El Precio Unitario debe ser mayor al costo')
        
        data = self.cleaned_data.get('dias_semana')
        if not data:  # Verifica que no sea vacío
            raise forms.ValidationError("Debes seleccionar al menos un dia de la semana")

        return cleaned_data

class CalendarForm(forms.Form):
    instructor = forms.ModelChoiceField(queryset=Instructor.objects.all(), label="Instructor")

class InstructorForm1(forms.Form):
    instructor = forms.ModelChoiceField(queryset=Instructor.objects.all(), label="Instructor")

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Grupo

class GroupForm(forms.ModelForm):
    DIAS_SEMANA_CHOICES = [
        ('DO', 'Domingo'),
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miércoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sábado'),
    ]    
    dias_semana = forms.MultipleChoiceField(
        choices=DIAS_SEMANA_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'dias-semana-checkbox'}),
        label="Días de la semana",
        required=False
    )

    class Meta:
        model = Grupo
        fields = ['grupo', 'clase', 'instructor', 'observa', 'modalidad', 'costo', 'preciounitario', 
                  'minimo', 'maximo', 'duracion', 'horaInicio', 'horaTermino', 'estatus', 'dias_semana']
        widgets = {
            'observa': forms.Textarea(attrs={'rows': 2, 'cols': 90}),
        }

    def clean(self):
        cleaned_data = super().clean()
        instructor = cleaned_data.get('instructor')
        dias_semana = cleaned_data.get('dias_semana')
        hora_inicio = cleaned_data.get('horaInicio')
        hora_termino = cleaned_data.get('horaTermino')

        if not dias_semana:
            raise ValidationError("Debes seleccionar al menos un día de la semana.")

        if hora_inicio and hora_termino and instructor:
            # Obtener los grupos activos (estatus=True) del mismo instructor
            grupos_conflictivos = Grupo.objects.filter(
                instructor=instructor,
                estatus=True  # Solo consideramos los grupos activos
            ).exclude(pk=self.instance.pk)  # Excluir el grupo actual si es edición

            for grupo in grupos_conflictivos:
                # Convertir el JSONField de 'dias_semana' a una lista si es necesario
                dias_grupo = grupo.dias_semana if isinstance(grupo.dias_semana, list) else list(grupo.dias_semana.keys())

                # Verificar si hay intersección de días entre el grupo actual y los existentes
                if set(dias_semana) & set(dias_grupo):  # Si hay coincidencia en los días
                    # Validar si el horario se solapa
                    if hora_inicio < grupo.horaTermino and hora_termino > grupo.horaInicio:
                        raise ValidationError(
                            f"El instructor ya tiene un grupo en este horario ({grupo.horaInicio} - {grupo.horaTermino}) los días {', '.join(dias_grupo)}."
                        )

        return cleaned_data
