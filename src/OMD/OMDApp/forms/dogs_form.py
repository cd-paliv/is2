from django import forms
from OMDApp.validators.form_validator import (EmptyFieldValidator, NoNumbersFieldValidator,
                                              DogAgeValidator, ExistsEmailValidator)
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
        

class AdoptionForm(forms.Form):
    name = forms.CharField(label="Nombre Completo (*)",
                           widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputFullName',
                                                         'placeholder': 'Ingrese su nombre completo', 'required': 'True'}),
                                                         validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    email = forms.EmailField(label="Email(*)",
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'inputEmail',
                                                            'placeholder': 'Ingrese su email'}),
                                                            validators=[EmptyFieldValidator()])
    motive = forms.CharField(label="Motivo(*)",
                           widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputMotive',
                                                         'placeholder': 'Ingrese el motivo de la adopcion', 'required': 'True'}),
                                                         validators=[EmptyFieldValidator()])
