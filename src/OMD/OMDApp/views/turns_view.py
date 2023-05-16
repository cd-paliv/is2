from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from OMDApp.models import Turno
from OMDApp.decorators import email_verification_required
from OMDApp.forms.turns_form import (AskForTurnForm)

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