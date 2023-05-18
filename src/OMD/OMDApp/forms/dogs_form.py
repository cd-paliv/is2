from django import forms
from OMDApp.validators.form_validator import EmptyFieldValidator, NoNumbersFieldValidator
from OMDApp.models import Perro, PPEA
from django.utils.translation import gettext as _

class RegisterAdoptionDogForm(forms.ModelForm):
    name = forms.CharField(label="Nombre del perro(*)",
                           widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputDogName',
                                                         'placeholder': 'Ingresa el nombre del perro', 'required': 'True'}),
                                                         validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    breed = forms.CharField(label="Raza del perro(*)",
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogBreed',
                                                          'placeholder': 'Ingresa la raza del perro', 'required': 'True'}),
                                                          validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    color = forms.CharField(label="Color del perro(*)",
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogColor',
                                                          'placeholder': 'Ingresa el color del perro', 'required': 'True'}),
                                                          validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    zone = forms.CharField(label="Zona donde se encuentra del perro(*)",
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogZone',
                                                          'placeholder': 'Ingresa la zona del perro', 'required': 'True'}),
                                                          validators=[EmptyFieldValidator()])

    class Meta:
        model = PPEA
        fields = ("name", "breed", "color", "zone")