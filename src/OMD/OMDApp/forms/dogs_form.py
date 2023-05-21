from django import forms
from OMDApp.validators.form_validator import EmptyFieldValidator, NoNumbersFieldValidator, DogAgeValidator
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
    birthdate = forms.DateField(label="Fecha de nacimiento estimada del perro(*)",
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputDogBirthdate',
                                                              'placeholder': 'Ingresa la fecha de nacimiento estimada del perro',
                                                              'required': 'True'}), validators=[EmptyFieldValidator(), DogAgeValidator()])

    class Meta:
        model = PPEA
        fields = ("name", "breed", "color", "birthdate")