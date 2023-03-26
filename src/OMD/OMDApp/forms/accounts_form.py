from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


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