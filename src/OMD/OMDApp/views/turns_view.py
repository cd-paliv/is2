from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from OMDApp.models import Turno, Veterinario
from OMDApp.decorators import email_verification_required
from OMDApp.forms.turns_form import (AskForTurnForm)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.db.models import Q


# Create your views here
def turn_type_mapping():
    map = {
        'T': 'Turno normal',
        'C': 'Castración',
        'V': 'Vacunación',
        'O': 'Operacion',
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

            turn.solicited_by = request.user
            turn.save()
            messages.success(request, f'Solicitud de turno exitosa')
            return redirect(reverse("home"))
    else:
        form = AskForTurnForm()
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
    turnos = list(Turno.objects.filter(solicited_by=request.user).order_by('state', 'date', '-hour').exclude(state="AC"))
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