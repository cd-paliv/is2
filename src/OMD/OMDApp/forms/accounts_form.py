from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from OMDApp.models import Perro
from django.utils.translation import gettext as _
from OMDApp.validators.password_validation import SymbolValidator, NumberValidator, UppercaseValidator, MinimumLengthValidator
from OMDApp.validators.form_validator import (EmptyFieldValidator, NoNumbersFieldValidator, 
                                              GreaterThanZeroValidator, UserAgeValidator, DogAgeValidator,
                                              ExistsEmailValidator, ExistsDNIValidator, NumbersFieldValidator)


# Create your forms here.
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}))
    

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre(*)",
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputName',
                                                               'placeholder': 'Ingresa tu nombre'}),
                                                               validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    last_name = forms.CharField(label="Apellido(*)",
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputLastname',
                                                              'placeholder': 'Ingresa tu apellido'}),
                                                              validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    email = forms.EmailField(label="Email(*)",
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'inputEmail',
                                                            'placeholder': 'Ingresa tu email'}),
                                                            validators=[EmptyFieldValidator(), ExistsEmailValidator()])
    dni = forms.IntegerField(label="DNI(*)",
                             widget=forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'inputDNI',
                                                             'placeholder': 'Ingresa tu DNI'}),
                                                             validators=[EmptyFieldValidator(), GreaterThanZeroValidator(), ExistsDNIValidator(), NumbersFieldValidator()])
    birthdate = forms.DateField(label="Fecha de nacimiento(*)",
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'birthdate',
                                                              'placeholder': 'Ingresa tu fecha de nacimiento'}),
                                                              validators=[EmptyFieldValidator(), UserAgeValidator()])

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "dni", "birthdate", "image")


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre(*)",
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputName',
                                                               'placeholder': 'Ingresa tu nombre'}), validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    last_name = forms.CharField(label="Apellido(*)",
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputLastname',
                                                              'placeholder': 'Ingresa tu apellido'}), validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    birthdate = forms.DateField(label="Fecha de nacimiento(*)",
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'birthdate',
                                                              'placeholder': 'Ingresa tu fecha de nacimiento'}
                                                              ), validators=[EmptyFieldValidator(), UserAgeValidator()])

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "birthdate", "image")


class RegisterDogForm(forms.ModelForm):
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
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'birthdate',
                                                              'placeholder': 'Ingresa la fecha de nacimiento estimada del perro',
                                                              'required': 'True'}), validators=[EmptyFieldValidator(), DogAgeValidator()])
    bool_options = {(1, 'Si'), (0, 'No')}
    castrated = forms.ChoiceField(label="¿Está castrado/a?(*)", choices=bool_options, widget=forms.RadioSelect(attrs={'type': 'radio'}))
    gender_options = {('F', 'Femenino'), ('M', 'Masculino')}
    gender = forms.ChoiceField(label="Sexo(*)", choices=gender_options, widget=forms.RadioSelect(attrs={'type': 'radio'}))

    class Meta:
        model = Perro
        fields = ("name", "breed", "color", "birthdate", "castrated", "gender", "image")

    
class EditPasswordForm(forms.Form):
    password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}))
    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(),
                                   validators=[
                                       MinimumLengthValidator(),
                                       SymbolValidator(),
                                       NumberValidator(),
                                       UppercaseValidator(),
                                    ])
    repeat_new_password = forms.CharField(label='Repita nueva contraseña', widget=forms.PasswordInput())