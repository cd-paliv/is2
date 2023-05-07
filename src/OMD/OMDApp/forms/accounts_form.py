from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from OMDApp.models import Perro
from django.utils.translation import gettext as _
from OMDApp.validators.password_validation import SymbolValidator, NumberValidator, UppercaseValidator, MinimumLengthValidator


# Create your forms here.
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_details = get_user_model().objects.filter(email=email)
        if not user_details.exists():
            raise forms.ValidationError("No existe una cuenta para el mail ingresado")
        return email

class RegisterForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "dni", "birthdate")
        labels = {"email" : "Email(*)", "first_name" : "Nombre(*)", "last_name" : "Apellido(*)", "dni" : "DNI(*)",
                                                                            "birthdate" : "Fecha de nacimiento(*)"}

        widgets = {
            'email' : forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id' : 'inputEmail',
                                        'placeholder' : 'Ingresa tu email'}),
            'first_name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputName',
                                        'placeholder' : 'Ingresa tu nombre'}),
            'last_name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputLastname',
                                        'placeholder' : 'Ingresa tu apellido'}),
            'dni' : forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'inputDNI',
                                        'placeholder' : 'Ingresa tu DNI'}),
            'birthdate' : forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputBirthdate',
                                        'placeholder' : 'Ingresa tu fecha de nacimiento'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError(_('El nombre es obligatorio'), code="required")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError(_('El apellido es obligatorio'), code="required")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_('El email es obligatorio'), code="required")
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni:
            raise forms.ValidationError(_('El DNI es obligatorio'), code="required")
        return dni

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if not birthdate:
            raise forms.ValidationError(_('La fecha de nacimiento es obligatoria'), code="required")
        return birthdate

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        dni = cleaned_data.get('dni')
        if email and dni:
            if get_user_model().objects.filter(dni=dni).exists():
                raise forms.ValidationError(_('El DNI ya se encuentra registrado'), code="unique")
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError(_('El email ya se encuentra registrado'), code="unique")
        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "birthdate")

        widgets = {
            'first_name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputName',
                                        'placeholder' : 'Ingresa tu nombre'}),
            'last_name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputLastname',
                                        'placeholder' : 'Ingresa tu apellido'}),
            'birthdate' : forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputBirthdate',
                                        'placeholder' : 'Ingresa tu fecha de nacimiento'}),
        }

class RegisterDogForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ("name", "breed", "color", "birthdate")
        labels = {"name" : "Nombre del perro(*)", "breed" : "Raza del perro(*)", "color" : "Color del perro(*)",
                                                    "birthdate" : "Fecha de nacimiento estimada del perro(*)"}

        widgets = {
            'name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogName',
                                        'placeholder' : 'Ingresa el nombre del perro', 'required': 'True'}),
            'breed' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogBreed',
                                        'placeholder' : 'Ingresa la raza del perro', 'required': 'True'}),
            'color' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogColor',
                                        'placeholder' : 'Ingresa el color del perro', 'required': 'True'}),
            'birthdate' : forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputDogBirthdate',
                                        'placeholder' : 'Ingresa la fecha de nacimiento estimada del perro', 'required': 'True'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError(_('El nombre es obligatorio'), code="required")
        return name

    def clean_breed(self):
        breed = self.cleaned_data.get('breed')
        if not breed:
            raise forms.ValidationError(_('La raza es obligatoria'), code="required")
        return breed

    def clean_color(self):
        color = self.cleaned_data.get('color')
        if not color:
            raise forms.ValidationError(_('El color es obligatorio'), code="required")
        return color

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if not birthdate:
            raise forms.ValidationError(_('La fecha de nacimiento es obligatoria'), code="required")
        return birthdate

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        breed = cleaned_data.get('breed')
        color = cleaned_data.get('color')
        birthdate = cleaned_data.get('birthdate')
        if name and breed and color and birthdate:
            if Perro.objects.filter(name=name, breed=breed, color=color, birthdate=birthdate).exists():
                raise forms.ValidationError(_('El perro ya se encuentra registrado'), code="unique")
        return cleaned_data
    
class EditPasswordForm(forms.Form):
    password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput())
    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(),
                                   validators=[
                                       MinimumLengthValidator(),
                                       SymbolValidator(),
                                       NumberValidator(),
                                       UppercaseValidator(),
                                    ])
    repeat_new_password = forms.CharField(label='Repita nueva contraseña', widget=forms.PasswordInput())