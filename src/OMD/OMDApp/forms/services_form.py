from django import forms
from django.utils.translation import gettext as _
from OMDApp.models import Servicio
from django.core.validators import RegexValidator
from OMDApp.validators.form_validator import (EmptyFieldValidator, NoNumbersFieldValidator)

# Create your forms here.
class RegisterServiceForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre(*)",
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputName',
                                                               'placeholder': 'Ingrese el nombre'}),
                                                               validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    last_name = forms.CharField(label="Apellido(*)",
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputLastname',
                                                              'placeholder': 'Ingrese el apellido'}),
                                                              validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    email = forms.EmailField(label="Email(*)",
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'inputEmail',
                                                            'placeholder': 'Ingrese el email'}),
                                                            validators=[EmptyFieldValidator()])
    phone_regex = r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}$'
    phone = forms.CharField(label="Teléfono(*)", max_length=20,
                                   widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputPhone',
                                                                 'placeholder': 'Ingrese el número de teléfono'}),
                                   validators=[RegexValidator(phone_regex, message='Por favor, introduce un número de teléfono válido.')])
    plaza_options = {
        ('PM', 'Plaza Moreno'), ('PSM', 'Plaza San Martín'), ('PMA', 'Plaza Malvinas Argentinas (ex Islas Malvinas)'),
        ('PR', 'Plaza Rivadavia'), ('PV', 'Parque Vucetich'), ('PRO', 'Plaza Rocha'), ('PI', 'Plaza Italia'), ('PS', 'Parque Saavedra'),
        ('PMT', 'Plaza Matheu'), ('PE', 'Plaza España'), ('PSAR', 'Plaza Sarmiento'), ('PC', 'Parque Castelli'), ('PPE', 'Plaza Perón (ex Brandsen)'),
        ('PY', 'Plaza Yrigoyen'), ('PROS', 'Plaza Rosas (ex Máximo Paz)'), ('PA', 'Plaza Alsina'), ('PO', 'Plaza Olazábal'), ('PBE', 'Plaza Belgrano'),
        ('PG', 'Plaza Güemes'), ('PAI', 'Parque Alberti'), ('P19N', 'Plaza 19 de Noviembre'), ('PAZ', 'Plaza Azcuénaga'), ('PP', 'Plaza Paso'),
    }
    zone = forms.ChoiceField(label="Zona(*)", choices=plaza_options,
                             widget=forms.Select(attrs={'class': 'form-control','id': 'inputZone',
                                                        'placeholder': 'Seleccione la zona donde trabaja'}))


    class Meta:
        model = Servicio
        fields = ("first_name", "last_name", "email", "phone", "zone")

class ContactServiceForm(forms.Form):
    first_name = forms.CharField(label="Nombre(*)",
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputName',
                                                               'placeholder': 'Ingrese el nombre'}),
                                                               validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    last_name = forms.CharField(label="Apellido(*)",
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputLastname',
                                                              'placeholder': 'Ingrese el apellido'}),
                                                              validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    email = forms.EmailField(label="Email(*)",
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'inputEmail',
                                                            'placeholder': 'Ingrese el email'}),
                                                            validators=[EmptyFieldValidator()])