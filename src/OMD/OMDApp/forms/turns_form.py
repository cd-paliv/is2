from django import forms
from django.contrib.auth import get_user_model
from OMDApp.models import Turno, Evaluacion
from django.utils.translation import gettext as _
from OMDApp.validators.form_validator import (EmptyFieldValidator, FloatFieldValidator, 
                                                NumbersFieldValidator, TurnDateBetweenValidator, TurnDateTodayValidator,
                                                GreaterThanZeroValidator)


class AskForTurnForm(forms.ModelForm):
    typeChoices = (('T', 'Turno normal'), ('C', 'Castración'), ('VA', 'Vacunacion - Tipo A'), ('VB', 'Vacunacion - Tipo B'))
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
    
    def __init__(self, *args, **kwargs):
        user_dogs = kwargs.pop('user_dogs', None)
        super().__init__(*args, **kwargs)
        if user_dogs:
            dog_choices = [(dog.id, dog.name) for dog in user_dogs]
            self.fields['solicited_by'] = forms.ChoiceField(label="Perro a atender(*)", choices=dog_choices,
                                                    widget=forms.Select(attrs={'class': 'form-control', 'id': 'inputDog', 'placeholder': 'Seleccione el perro a atender'})
            )

    class Meta:
        model = Turno
        fields = ("type", "hour", "date", "motive", "solicited_by")

class AttendTurnForm(forms.Form):
    weight = forms.FloatField(label="Peso", localize=True, 
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

class AttendUrgencyForm(forms.Form):
    weight = forms.FloatField(label="Peso", localize=True, 
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

    def __init__(self, urgency_choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if urgency_choices:
            self.fields['urgency_choices'] = forms.MultipleChoiceField(
                label="Intervenciones permitidas",
                choices=urgency_choices.items(),
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                required=False
            )

class EvaluationForm(forms.Form):
    CHOICES = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")]
    Evaluacion      = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    observations = forms.CharField(label="Observaciones de la consulta(*)",
                           widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control','id': 'inputMotive',
                                                         'placeholder': 'Ingrese observaciones sobre la atención', 'required': 'True'}),
                                                         validators=[EmptyFieldValidator()])
    bool_options = {(1, 'Si'), (0, 'No')}
    anonimous = forms.ChoiceField(label="¿Valorar como anonimo?(*)", choices=bool_options, widget=forms.RadioSelect(attrs={'type': 'radio'}))
