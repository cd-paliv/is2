from django import forms
from OMDApp.models import Campana, Donacion, Tarjeta
from OMDApp.validators.form_validator import (EmptyFieldValidator, NoNumbersFieldValidator,GreaterThanZeroValidator, NumbersFieldValidator, CampaignDateValidator)


class RegisterDonationEventsForm(forms.ModelForm):
    name = forms.CharField(label="Nombre del evento(*)",
                           widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputCampName',
                                                         'placeholder': 'Ingresa el nombre del evento', 'required': 'True'}),
                                                         validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
    estimated_amount = forms.FloatField(label= "Monto esperado a recaudar(*)",widget= forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'inputAmount',
                                                             'placeholder': 'Ingrese el monto esperado a recaudar'}),
                                                             validators=[EmptyFieldValidator(), GreaterThanZeroValidator(), NumbersFieldValidator()])
    date_in = forms.DateField(label="Fecha de inicio del evento(*)",
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputDateIn',
                                                              'placeholder': 'Ingresa la fecha de inicio del evento',
                                                              'required': 'True'}), validators=[EmptyFieldValidator(), CampaignDateValidator()])
    date_out = forms.DateField(label="Fecha de fin del evento(*)",
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputDateOut',
                                                              'placeholder': 'Ingresa la fecha de fin de evento',
                                                              'required': 'True'}), validators=[EmptyFieldValidator(), CampaignDateValidator()])
    class Meta:
        model = Campana
        fields = ("name", "date_in", "date_out", "estimated_amount")
        
class RegisterDonationForm(forms.ModelForm):
   name = forms.CharField(label = "Nombre del donador(*)",
                          widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputDonName',
                                                         'placeholder': 'Ingresa el nombre del donador', 'required': 'True'}),
                                                         validators=[EmptyFieldValidator(), NoNumbersFieldValidator()])
   email = forms.EmailField(label="Email(*)",
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', 'id': 'inputEmail',
                                                            'placeholder': 'Ingrese su email'}),
                                                            validators=[EmptyFieldValidator()])
   message = forms.CharField(label="Mensaje", required=False,
                             widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputMessage',
                                                         'placeholder': 'Ingrese mensaje'}))
   amount = forms.FloatField(label= "Monto a donar(*)",
                             widget= forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'inputAmount',
                                                             'placeholder': 'Ingrese el monto a donar'}),
                                                             validators=[EmptyFieldValidator(), GreaterThanZeroValidator(), NumbersFieldValidator()])
   class Meta:
        model = Donacion
        fields = ("name", "email", "amount")

class RegisterCardForm(forms.ModelForm):
   holder = forms.CharField(label = "Titular(*)",
                          widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputNameCard',
                                                         'placeholder': 'Ingresa el nombre del titular de la tarjeta', 'required': 'True'}),
                                                         validators=[EmptyFieldValidator(), NoNumbersFieldValidator()]) 
   number = forms.IntegerField(label = "Numero de tarjeta(*)",
                                    widget= forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'inputCardNumber',
                                                             'placeholder': 'Ingrese su tarjeta'}),
                                                             validators=[EmptyFieldValidator(), GreaterThanZeroValidator(), NumbersFieldValidator()])
   security_number = forms.IntegerField(label="Numero de seguridad de la tarjeta(*)",
                                             widget=forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'inputCardNumberSecurity',
                                                             'placeholder': 'Ingrese su numero de seguridad de la tarjeta'}),
                                                             validators=[EmptyFieldValidator(), GreaterThanZeroValidator(), NumbersFieldValidator()])
   expiration = forms.DateField(label="Fecha de vencimiento de la tarjeta(*)",
                                widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputExpiration',
                                                              'placeholder': 'Ingresa la fecha de vencimiento de la tarjeta',
                                                              'required': 'True'}), validators=[EmptyFieldValidator()])

   class Meta:
        model = Tarjeta
        fields = ("holder", "number", "security_number", "expiration")