from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from OMDApp.models import Perro


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
        labels = {"email" : "Email(*)", "first_name" : "Nombre(*)", "last_name" : "Apellido(*)", "dni" : "DNI(*)","birthdate" : "Fecha de nacimiento(*)"}

        widgets = {
            'email' : forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id' : 'inputEmail',
                                        'placeholder' : 'Ingresa tu email', 'required': 'True'}),
            'first_name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputName',
                                        'placeholder' : 'Ingresa tu nombre', 'required': 'True'}),
            'last_name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputLastname',
                                        'placeholder' : 'Ingresa tu apellido', 'required': 'True'}),
            'dni' : forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'inputDNI',
                                        'placeholder' : 'Ingresa tu DNI', 'required': 'True'}),
            'birthdate' : forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputBirthdate',
                                        'placeholder' : 'Ingresa tu fecha de nacimiento', 'required': 'True'}),
        }

        error_messages = {
            'email': {
                'unique' : {'Registro fallido. El email ya se encuentra registrado'}
            },
            'dni': {
                'unique' : {'Registro fallido. El DNI ya se encuentra registrado'}
            }
        }

class RegisterDogForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ("name", "breed", "color", "birthdate", "observations")
        labels = {"name" : "Nombre del perro(*)", "breed" : "Raza del perro(*)", "color" : "Color del perro(*)", "birthdate" : "Fecha de nacimiento estimada del perro(*)", "observations" : "Observaciones sobre el perro"}

        widgets = {
            'name' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogName',
                                        'placeholder' : 'Ingresa el nombre del perro', 'required': 'True'}),
            'breed' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogBreed',
                                        'placeholder' : 'Ingresa la raza del perro', 'required': 'True'}),
            'color' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputDogColor',
                                        'placeholder' : 'Ingresa el color del perro', 'required': 'True'}),
            'birthdate' : forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputDogBirthdate',
                                        'placeholder' : 'Ingresa la fecha de nacimiento estimada del perro', 'required': 'True'}),
            'observations' : forms.Textarea(attrs={"rows" : 3, "cols" : 10, 'type': 'text', 'class': 'form-control', 'id': 'inputDogObservations',
                                        'placeholder' : 'Ingresa observaciones del perro', 'required': 'False'}),
        }