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

    class Meta:
        model = Servicio
        fields = ("first_name", "last_name", "email", "phone")

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