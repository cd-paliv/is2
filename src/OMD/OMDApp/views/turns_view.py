from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from OMDApp.models import Turno
from OMDApp.decorators import email_verification_required
from OMDApp.forms.turns_form import (AskForTurnForm)
from django.views.generic import ListView
from django.views import View


# Create your views here

@login_required
@email_verification_required
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


class AcceptTurnsView(ListView):
    login_url = '/login/'
    model = Turno
    template_name = 'turns/acceptTurns.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        turns = Turno.objects.filter(status=False)
        turn_list = []
        for turn in turns:
            turn_list.append({
                'type' : turn.type,
                'hour': turn.hour,
                'date': turn.date,
                'motive': turn.motive
            })
        context['turn_list'] = turn_list
        context['one_turn'] = len(turn_list) == 1
        return context
        #return render(request, 'turns/ask_for_turn.html', {'form': form})

def ViewPendingTurns(request):
    turnos = list(Turno.objects.filter(state="S")) # solicited
    return render(request, "turns/acceptTurns.html", {"turn_list" : turnos})