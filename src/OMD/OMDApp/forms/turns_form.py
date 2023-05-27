from django import forms
from django.contrib.auth import get_user_model
from OMDApp.models import Turno
from django.utils.translation import gettext as _
from OMDApp.validators.form_validator import (EmptyFieldValidator, FloatFieldValidator, 
                                                NumbersFieldValidator, TurnDateBetweenValidator, TurnDateTodayValidator,
                                                GreaterThanZeroValidator)


class AskForTurnForm(forms.ModelForm):
    typeChoices = (('T', 'Turno normal'), ('C', 'Castracion'), ('VA', 'Vacunacion - Tipo A'), ('VB', 'Vacunacion - Tipo B'), ('O', 'Operacion'))
    type = forms.ChoiceField(label="Tipo(*)", choices=typeChoices,
                             widget=forms.Select(attrs={'class': 'form-control','id': 'inputType',
                                                        'placeholder': 'Seleccione el tipo de turno'}))
    hourChoices = (('Morning', 'Tanda mañana: 08:00 a 13:00hs'),('Afternoon', 'Tanda tarde: 15:00 a 20:00hs'),)
    hour = forms.ChoiceField(label="Horario(*)", choices=hourChoices,
                             widget=forms.Select(attrs={'class': 'form-control','id': 'inputHour',
                                                        'placeholder': 'Seleccione el horario del turno'}))
    date = forms.DateField(label="Fecha(*)",
                            widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control', 'id': 'inputDate',
                                                            'placeholder': 'Ingrese la fecha en la que quiera pedir el turno'}),
                                                            validators=[EmptyFieldValidator(), TurnDateBetweenValidator(), TurnDateTodayValidator()])
    motive = forms.CharField(label="Razon(*)",
                             widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputMotivo',
                                                         'placeholder': 'Ingrese la razon por la cual quiere su turno'}),
                                                         validators=[EmptyFieldValidator()])
    
    class Meta:
        model = Turno
        fields = ("type", "hour", "date", "motive")
        labels = {
            "type": "Tipo(*)",
            "hour": "Horario(*)",
            "date": "Fecha(*)",
            "motive": "Razon(*)",
        }

class AttendTurnForm(forms.Form):
    weight = forms.FloatField(label="Peso",
                               widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputPeso',
                                                             'placeholder': 'Ingrese el peso del perro'}),
                                                             validators=[FloatFieldValidator()])
    observations = forms.CharField(label="Observaciones",
                               widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputObservaciones',
                                                             'placeholder': 'Ingrese observaciones sobre la atención'}))
    amount = forms.FloatField(label="Costo(*)",
                               widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'inputCosto',
                                                             'placeholder': 'Ingrese el costo de la atención'}),
                                                             validators=[EmptyFieldValidator(), GreaterThanZeroValidator(), FloatFieldValidator()])