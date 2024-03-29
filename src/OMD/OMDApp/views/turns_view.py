from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from OMDApp.models import Turno, Veterinario, Perro, Donacion
from OMDApp.decorators import email_verification_required
from OMDApp.forms.turns_form import (AskForTurnForm, AttendTurnForm, EvaluationForm, AttendUrgencyForm)
from django.views.decorators.cache import cache_control
from django.db.models import Q
from datetime import date
import json
from OMDApp.views.helpers import (turn_type_mapping, turn_hour_mapping, actual_turn_hour_check, turn_type_mapping_with_urgency,
                                    generate_date, append_data, delete_unwanted_next_turns, get_filtered_interventions,
                                    get_days_until_next_turn, convert_days_to_date)
from datetime import datetime
from decimal import Decimal


# Create your views here

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

            if Turno.objects.filter(solicited_by=turn.solicited_by, date=turn.date).exists():
                messages.error(request, "No puede solicitar un turno para la misma fecha con el mismo perro dos veces")
                return redirect(reverse("askForTurn"))

            if turn.type not in get_filtered_interventions(turn.solicited_by):
                if turn.type == 'C':
                    messages.error(request, "No puede solicitar un turno de castración para un perro castrado")
                    return redirect(reverse("askForTurn"))
                
                if turn.type == 'D':
                    has_desp_turn = True if Turno.objects.filter(date=date.today(), type='D').exists() else False
                    if has_desp_turn:
                        messages.error(request, "No puede solicitar mas de un turno de desparasitación por día para el mismo perro")
                        return redirect(reverse("askForTurn"))
                
                if turn.type == 'VA' or turn.type == 'VB':
                    time = get_days_until_next_turn(turn.solicited_by, turn.type)
                    if time is not None:
                        turn_type = str(turn_type_mapping().get(turn.type))
                        messages.error(request, "El perro debe esperar %s días para volver a recibir una %s" % (time, turn_type))
                        return redirect(reverse("askForTurn"))

            same_date_turns = list(Turno.objects.filter(date=turn.date, hour=turn.hour))
            if len(same_date_turns) == 20:
                hours = str(turn_hour_mapping().get(turn.hour)).split(': ')[1]
                message = 'No quedan turnos disponibles el %s de %s' % (turn.date.strftime('%d/%m/%Y'), hours)
                messages.error(request, message)
                return redirect(reverse("askForTurn"))

            turn.save()
            if turn.type != 'T':
                delete_unwanted_next_turns(turn.solicited_by, turn.type)

            messages.success(request, f'Solicitud de turno exitosa')
            return redirect(reverse("home"))
        else:
            form.fields['solicited_by'].choices = [(dog.id, dog.name) for dog in Perro.objects.filter(owner=request.user)]
            form.data = form.data.copy()
    else:
        user_dogs = Perro.objects.filter(owner=request.user)
        form = AskForTurnForm(user_dogs=user_dogs)
    return render(request, 'turns/ask_for_turn.html', {'form': form})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ViewPendingTurns(request):
    turnos = list(Turno.objects.filter(state="S").order_by('-hour', 'date').exclude(type="U")) # solicited
    return render(request, "turns/turn_list.html", {"turn_list" : turnos, "turns" : "P",
                                                    'turn_type_mapping': turn_type_mapping(), 'turn_hour_mapping': turn_hour_mapping()})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ViewAcceptedTurns(request):
    turnos = list(Turno.objects.filter(state="A").order_by('-hour', 'date').exclude(type="U")) # accepted
    return render(request, "turns/turn_list.html", {"turn_list" : turnos, "turns" : "A", "todays_date": date.today(),
                                                    'turn_type_mapping': turn_type_mapping(), 'turn_hour_mapping': turn_hour_mapping()})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AcceptTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)
    turn.state = "A"
    turn.accepted_by = Veterinario.objects.get(user=request.user)
    turn.save()

    soliciter = get_user_model().objects.get(id=turn.solicited_by.owner.id)
    hours = str(turn_hour_mapping().get(turn.hour)).split(': ')[1]
    turn_type = str(turn_type_mapping().get(turn.type))
    message = 'Se ha aceptado su turno de %s del %s a las %s en Oh My Dog' % (turn_type, turn.date.strftime('%d/%m/%Y'), hours)
    soliciter.email_user('Cambio en estado de turno', message)

    messages.success(request, "Turno aceptado")
    return redirect(reverse("pendingTurns"))

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RejectTurn(request, turn_id):
    motive = request.POST.get('motive')
    print(motive)
    turn = Turno.objects.get(id=turn_id)

    soliciter = get_user_model().objects.get(id=turn.solicited_by.owner.id)
    hours = str(turn_hour_mapping().get(turn.hour)).split(': ')[1]
    turn_type = str(turn_type_mapping().get(turn.type))
    message = 'Se ha rechazado su turno de %s del %s a las %s en Oh My Dog.' % (turn_type, turn.date.strftime('%d/%m/%Y'), hours)
    if motive:
        message += '\n\nMotivo: %s' % motive
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
    turnos = list(Turno.objects.filter(solicited_by__in=dogs).order_by('state', 'date', '-hour').exclude(state="F").exclude(type="U"))
    return render(request, "turns/turn_list.html", {"turn_list" : turnos, "turns" : "U",
                                                    'turn_type_mapping': turn_type_mapping(), 'turn_hour_mapping': turn_hour_mapping()})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def CancelTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)

    if turn.state == 'A' and turn.date == date.today():
        messages.error(request, "No puede cancelar un turno para hoy que ya fue aceptado")
        return redirect(reverse("myTurns"))

    soliciter = get_user_model().objects.get(id=turn.solicited_by.owner.id)
    hours = str(turn_hour_mapping().get(turn.hour)).split(': ')[1]
    turn_type = str(turn_type_mapping().get(turn.type))
    message = 'Usted ha cancelado su turno de \'%s\' del %s a las %s en Oh My Dog' % (turn_type, turn.date.strftime('%d/%m/%Y'), hours)
    soliciter.email_user('Cambio en estado de turno', message)

    if turn.accepted_by is not None:
        vet = Veterinario.objects.get(id=turn.accepted_by.id)
        message_vet = 'Se ha cancelado un turno de "%s" del %s a las %s en Oh My Dog' % (turn_type, turn.date.strftime('%d/%m/%Y'), hours)
        vet.user.email_user('Cambio en estado de turno', message_vet)

    turn.delete()

    messages.success(request, "Turno cancelado")
    return redirect(reverse("myTurns"))

def get_discount(user_id, total):
    user = get_user_model().objects.get(id=user_id)
    donations = Donacion.objects.filter(usuario=user, used=0)
    total_donated = 0
    for donation in donations:
        total_donated += donation.amount

    if total_donated != 0:
        discount_limit = Decimal(total) * Decimal('0.5')
        discount_amount = min(Decimal(total_donated) * Decimal('0.2'), discount_limit)
        discount_percentage = (discount_amount * total) / Decimal('100') if discount_amount != discount_limit else 50
        discounted_total = Decimal(total) - discount_amount
        donations.update(used=1)

        return discount_percentage, discounted_total
    else:
        return 0, 0

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AttendTurnView(request, turn_id, urgency=False):
    if request.session.get('show_finalized_turn_visited'):
        #del request.session['show_finalized_turn_visited']
        return redirect(reverse('home'))
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
            turn.save()

            if turn.type == 'VA' or turn.type == 'VB':
                turn.add_to_health_book()

                # Automatic new vacunation turn
                new_date = convert_days_to_date(dog, turn.type)
                motive = f"Generación automática de turno para vacunación tipo {'A' if turn.type == 'VA' else 'B'}"
                Turno.objects.create(state='S', type=turn.type, hour=turn.hour, date=new_date, motive=motive, solicited_by=dog)

            elif turn.type == 'C':
                Perro.objects.filter(id=dog.id).update(castrated=True)
                turn.add_to_health_book()
            
            elif turn.type == 'D':
                turn.add_to_health_book()
            
            turn.add_to_clinic_history()

            messages.success(request, "Turno finalizado")
            return redirect(reverse('showFinalizedTurn', kwargs={'turn_id': turn.id}))
        else:
            form.data = form.data.copy()
    else:
        form = AttendTurnForm(initial={'weight': dog.weight})
    return render(request, "turns/attend_turn.html", {'form': form, 'dog': dog})

from django.utils.html import format_html

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ShowFinalizedTurn(request, turn_id):
    turn = Turno.objects.get(id=turn_id)
    actual_amount = turn.amount
    discount_percentage, discounted_total = get_discount(turn.solicited_by.owner.id, turn.amount)
    if discounted_total != 0:
        turn.amount = discounted_total
        turn.save()

    request.session['show_finalized_turn_visited'] = True

    message = render_to_string("turns/turn_evaluate_mail.html", {'dia': turn.date, 'perro': turn.solicited_by.name,
                                        'absolute_url': request.build_absolute_uri(reverse('evaluation', kwargs={'turn_id': turn.id})) })

    turn.solicited_by.owner.email_user("Encuesta de evaluación de servicio", message)

    return render(request, "turns/turn_view.html", {'turn': turn, 'actual_amount': actual_amount, 'discounted_total': discounted_total,
                                                    'discount_percentage': discount_percentage,'turn_type_mapping': turn_type_mapping_with_urgency(),
                                                    'turn_hour_mapping': turn_hour_mapping()})


@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def NewUrgencyButtonView(request):
    #if actual_turn_hour_check() is None:
    #    messages.error(request, 'No puede generar una nueva urgencia fuera de horario de atencion')
    #    return redirect(reverse('home'))
    
    return render(request, 'turns/select_urgency.html')

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def GenerateUrgencyView(request, dog_id):
    dog = Perro.objects.get(id=dog_id)
    turn = Turno.objects.create(type='U', hour=actual_turn_hour_check(), date=date.today(), motive='Urgencia',
                                solicited_by=dog, urgency_turns=json.dumps([]), accepted_by=Veterinario.objects.get(user=request.user))

    return redirect(reverse("attendUrgency", kwargs={"turn_id": turn.id}))

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AttendUrgencyView(request, turn_id):
    if request.session.get('show_finalized_turn_visited'):
        #del request.session['show_finalized_turn_visited']
        return redirect(reverse('home'))
    turn = Turno.objects.get(id=turn_id)
    dog = turn.solicited_by
    urgency_choices = get_filtered_interventions(dog)
    if request.method == "POST":
        form = AttendUrgencyForm(data=request.POST, urgency_choices=urgency_choices)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            Perro.objects.filter(id=dog.id).update(weight=weight)

            turn.observations = form.cleaned_data['observations']
            turn.amount = form.cleaned_data['amount']
            turn.state = 'F'
            turn.finalized_at = date.today()

            turn.save()
            turn.add_to_health_book()
            turn.add_to_clinic_history()

            # Add urgency interventions
            allowed_choices = request.POST.getlist('urgency')
            for key in allowed_choices:
                GenerateTurnForUrgencyView(turn.id, request.user, turn.solicited_by, key)

            # Delete turns
            for intervention in turn.urgency_turns:
                delete_unwanted_next_turns(turn.solicited_by, intervention)

            return redirect(reverse('showFinalizedTurn', kwargs={'turn_id': turn.id}))
        else:
            form.data = form.data.copy()
    else:
        form = AttendUrgencyForm(urgency_choices=urgency_choices, initial={'weight': dog.weight})
        #form = AttendTurnForm(initial={'weight': dog.weight})
    return render(request, "turns/attend_turn.html", {'form': form, 'dog': dog, 'type': 'U', 'turn_id': turn.id,
                                                      'urgency_choices': get_filtered_interventions(dog)})

def GenerateTurnForUrgencyView(turn_id, vet, dog, opt):
    turn = Turno.objects.get(id=turn_id)
    if opt == 'VA' or opt == 'VB':
        # Generate vacunation turn
        motive = f"Vacunación tipo {'A' if opt == 'VA' else 'B'} realizada en urgencia"
        vacc_turn = Turno.objects.create(state='F', type=opt, hour=datetime.now().time(), date=turn.date, motive=motive, solicited_by=dog,
                                         accepted_by=Veterinario.objects.get(user=vet), amount=0.0, finalized_at = date.today())
        vacc_turn.add_to_health_book()

        # Create new vaccination turn
        if turn.solicited_by.owner.email_confirmed:
            new_date = convert_days_to_date(vacc_turn.solicited_by, vacc_turn.type)
            new_motive = f"Generación automática de turno para vacunación tipo {'A' if opt == 'VA' else 'B'}"
            Turno.objects.create(state='S', type=opt, hour=turn.hour, date=new_date, motive=new_motive, solicited_by=dog)

    elif opt == 'C':
        # Generate castration turn
        motive = f"Castración realizada en urgencia"
        cast_turn = Turno.objects.create(state='F', type=opt, hour=datetime.now().time(), date=turn.date, motive=motive, solicited_by=dog,
                                         accepted_by=Veterinario.objects.get(user=vet), amount=0.0, finalized_at = date.today())
        cast_turn.add_to_health_book()
        #cast_turn.add_to_clinic_history()

        # Update dog
        Perro.objects.filter(id=dog.id).update(castrated=True)
    
    elif opt == 'D':
        motive = f"Desparasitación realizada en urgencia"
        desp_turn = Turno.objects.create(state='F', type=opt, hour=datetime.now().time(), date=turn.date, motive=motive, solicited_by=dog,
                                         accepted_by=Veterinario.objects.get(user=vet), amount=0.0, finalized_at = date.today())
        desp_turn.add_to_health_book()

    # Add new intervention to urgency
    append_data(turn, opt)

from django.template.loader import render_to_string

@cache_control(max_age=3600, no_store=True)
def Evaluation(request, turn_id):
    if  request.method == 'POST':
        eva = EvaluationForm(request.POST)
        if eva.is_valid():
            turn = Turno.objects.get(id=turn_id)
            data_dict = eva.cleaned_data

            print(data_dict['anonymus'])

            message = render_to_string('turns/turn_evaluated_email.html', {'eva': data_dict, 'turn': turn})
            turn.accepted_by.user.email_user("Se ha evaluado su atención", message)

            return redirect(reverse("home"))
        else:
            eva.data = eva.data.copy
    else:
        eva = EvaluationForm()
    return render(request, 'turns/evaluate.html', {'form':eva})