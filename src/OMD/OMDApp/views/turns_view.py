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


# Create your views here

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AskForTurn(request):
    if request.method == "POST":
        form = AskForTurnForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Solicitud de turno exitosa')
            return redirect(reverse("home"))
    else:
        form = AskForTurnForm()
    return render(request, 'turns/ask_for_turn.html', {'form': form})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ViewPendingTurns(request):
    turnos = list(Turno.objects.filter(state="S")) # solicited
    return render(request, "turns/acceptTurns.html", {"turn_list" : turnos, "pending" : True})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ViewAcceptedTurns(request):
    turnos = list(Turno.objects.filter(state="A")) # accepted
    return render(request, "turns/acceptTurns.html", {"turn_list" : turnos, "pending" : False})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AcceptTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)
    turn.state = "A"
    turn.accepted_by = Veterinario.objects.get(user=request.user)
    turn.save()

    soliciter = get_user_model().objects.get(id=turn.solicited_by.id)
    soliciter.email_user('Cambio en estado de turno', 'Se ha aceptado su turno en Oh My Dog')

    messages.success(request, "Turno aceptado")
    return redirect(reverse("pendingTurns"))

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RejectTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)

    soliciter = get_user_model().objects.get(id=turn.solicited_by.id)
    soliciter.email_user('Cambio en estado de turno', 'Se ha rechazado su turno en Oh My Dog')

    turn.delete()

    messages.success(request, "Turno rechazado")
    return redirect(reverse("pendingTurns"))