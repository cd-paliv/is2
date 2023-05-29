from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from OMDApp.models import Turno, Veterinario, Perro
from OMDApp.decorators import email_verification_required, vet_required
from OMDApp.forms.turns_form import (AskForTurnForm, AttendTurnForm)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.db.models import Q


# Create your views here
def turn_type_mapping():
    map = {
        'T': 'Turno normal',
        'C': 'Castración',
        'VA': 'Vacunación - Tipo A',
        'VB': 'Vacunacion - Tipo B',
        'U': 'Urgencia',
    }
    return map

def turn_hour_mapping():
    map = {
        'Morning': 'Tanda mañana: 08:00 a 13:00hs',
        'Afternoon': 'Tanda tarde: 15:00 a 20:00hs',
    }
    return map

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AskForTurn(request):
    if request.method == "POST":
        form = AskForTurnForm(request.POST)
        if form.is_valid():
            turn = form.save(commit=False)

            same_date_turns = list(Turno.objects.filter(date=turn.date, hour=turn.hour))
            if len(same_date_turns) == 20:
                hours = str(turn_hour_mapping().get(turn.hour)).split(': ')[1]
                message = 'No quedan turnos disponibles el %s de %s' % (turn.date.strftime('%d/%m/%Y'), hours)
                messages.error(request, message)
                return redirect(reverse("askForTurn"))

            turn.save()
            messages.success(request, f'Solicitud de turno exitosa')
            return redirect(reverse("home"))
    user_dogs = Perro.objects.filter(owner=request.user)
    form = AskForTurnForm(user_dogs=user_dogs)
    return render(request, 'turns/ask_for_turn.html', {'form': form})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ViewPendingTurns(request):
    turnos = list(Turno.objects.filter(state="S").order_by('-hour', 'date')) # solicited
    return render(request, "turns/turn_list.html", {"turn_list" : turnos, "turns" : "P",
                                                    'turn_type_mapping': turn_type_mapping(), 'turn_hour_mapping': turn_hour_mapping()})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ViewAcceptedTurns(request):
    turnos = list(Turno.objects.filter(Q(state="A") | Q(state="AC")).order_by('-hour', 'date')) # accepted
    return render(request, "turns/turn_list.html", {"turn_list" : turnos, "turns" : "A",
                                                    'turn_type_mapping': turn_type_mapping(), 'turn_hour_mapping': turn_hour_mapping()})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AcceptTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)
    turn.state = "A"
    turn.accepted_by = Veterinario.objects.get(user=request.user)
    turn.save()

    soliciter = get_user_model().objects.get(id=turn.solicited_by.id)
    message = 'Se ha aceptado su turno del %s en Oh My Dog' % turn.date.strftime('%d/%m/%Y')
    soliciter.email_user('Cambio en estado de turno', message)

    messages.success(request, "Turno aceptado")
    return redirect(reverse("pendingTurns"))

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RejectTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)

    soliciter = get_user_model().objects.get(id=turn.solicited_by.id)
    message = 'Se ha rechazado su turno del %s en Oh My Dog' % turn.date.strftime('%d/%m/%Y')
    soliciter.email_user('Cambio en estado de turno', message)

    turn.delete()

    messages.success(request, "Turno rechazado")
    return redirect(reverse("pendingTurns"))

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ViewMyTurns(request):
    user = request.user
    dogs = Perro.objects.filter(owner=user)
    turnos = list(Turno.objects.filter(solicited_by__in=dogs).order_by('state', 'date', '-hour').exclude(Q(state="F") | Q(state="AC")))
    return render(request, "turns/turn_list.html", {"turn_list" : turnos, "turns" : "U",
                                                    'turn_type_mapping': turn_type_mapping(), 'turn_hour_mapping': turn_hour_mapping()})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def CancelTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)
    if turn.state == "A":
        turn.state = "AC"
        turn.save()
    else:
        turn.delete()

    soliciter = get_user_model().objects.get(id=turn.solicited_by.id)
    message = 'Usted ha cancelado su turno del %s en Oh My Dog' % turn.date.strftime('%d/%m/%Y')
    soliciter.email_user('Cambio en estado de turno', message)

    messages.success(request, "Turno cancelado")
    return redirect(reverse("myTurns"))

from datetime import date, timedelta

def generate_date(today, birthdate, type):
    if type == 'VA':
        months_diff = (today.year - birthdate.year) * 12 + (today.month - birthdate.month)
    else:
        months_diff = 4 # default 365 days for type B

    if months_diff < 4:
        future_date = today + timedelta(days=21)
    else:
        future_date = today + timedelta(days=365)

    return future_date


@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AttendTurnView(request, turn_id):
    turn = Turno.objects.get(id=turn_id)
    dog = turn.solicited_by
    if request.method == "POST":
        form = AttendTurnForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            Perro.objects.filter(id=dog.id).update(weight=weight)

            turn.observations = form.cleaned_data['observations']
            turn.amount = form.cleaned_data['amount']
            turn.state = 'F'
            turn.finalized_at = date.today()

            if turn.type == 'VA' or turn.type == 'VB':
                turn.add_to_health_book()

                # Generación automática de nuevo turno para vacunación
                new_date = generate_date(turn.date, dog.birthdate, type=turn.type)
                motive = f"Generación automática de turno para vacunación tipo {'A' if turn.type == 'VA' else 'B'}"
                Turno.objects.create(state='S', type=turn.type, hour=turn.hour, date=new_date, motive=motive, solicited_by=dog)

            elif turn.type == 'C':
                turn.castrated = True
                turn.add_to_health_book()
                
            elif turn.type == 'U':
                turn.add_to_health_book()
            
            turn.save()
            turn.add_to_clinic_history()
            return redirect(reverse('home'))
        else:
            form.data = form.data.copy()
    else:
        form = AttendTurnForm(initial={'weight': dog.weight})
    return render(request, "turns/attend_turn.html", {'form': form, 'dog': dog})