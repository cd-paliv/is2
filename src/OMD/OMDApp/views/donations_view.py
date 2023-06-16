from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from OMDApp.models import Campana,Donacion, Tarjeta
from django.contrib.auth.decorators import login_required
from OMDApp.forms.donations_form import RegisterDonationForm,RegisterCardForm, RegisterDonationEventsForm
from OMDApp.decorators import email_verification_required
from django.views.decorators.cache import cache_control
from datetime import date

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RegisterEvent(request):
    if request.method == 'POST':
        form = RegisterDonationEventsForm(request.POST)
        if form.is_valid():
            camp = form.save(commit=False)
            camp.name = camp.name.title()

            if Campana.objects.filter(name__iexact=camp.name, date_in=camp.date_in, date_out=camp.date_out).exists():
                messages.error(request, "Ya existe una campaña de donación con el nombre ingresado en las fechas ingresadas")
                return redirect(reverse("viewCampaigns"))
            
            camp.save()
            messages.success(request, 'Registro de campaña exitoso')
            return redirect(reverse("home"))
        else:
            form.data = form.data.copy()
    else:
        form = RegisterDonationEventsForm()
    return render(request, 'donations/create_donation.html', {'form': form})

def ViewCampaigns(request):
    campanas = list(Campana.objects.filter(state='V').order_by('name'))
    return render(request, "donations/view_donations.html", {"view_donations" : campanas})

def ViewFinalizedCampaigns(request):
    campanas = list(Campana.objects.filter(state='F').order_by('name'))
    return render(request, "donations/view_donations.html", {"view_donations" : campanas, "view_finalized_donations": True})


@cache_control(max_age=3600, no_store=True)
def InsertCardView(request):
    if request.method == 'POST':
        form = RegisterCardForm(request.POST)
        if form.is_valid():
            # Create Donacion
            campana_id = request.session.get('camp_id')
            don_data = request.session.get('don_data')
            don_data['campana'] = Campana.objects.get(id=campana_id)
            don = Donacion.objects.create(**don_data)

            # Change data
            don.name = don.name.title()
            don.message = don.message.capitalize()
            don.usuario = request.user if request.user.is_authenticated else None
            don.save()
            
            # Save card
            card = form.save(commit=False)

            card.from_donation = don
            card.save()

            # Update campaign data
            camp = Campana.objects.get(id=campana_id)
            camp.colected_amount = camp.colected_amount + don.amount
            if camp.colected_amount >= camp.estimated_amount:
                camp.state = 'F'
            camp.save()

            # Remove session data
            del request.session['don_data']
            del request.session['camp_id']
            
            messages.success(request, 'Donación realizada')
            return redirect(reverse("home"))
        else:
            form.data = form.data.copy()
    else:
        form = RegisterCardForm()
    return render(request, 'donations/payment.html', {'form': form})

@cache_control(max_age=3600, no_store=True)
def RegisterDonation(request, campana_id):
    if  request.method == 'POST':
        donation = RegisterDonationForm(request.POST)
        if donation.is_valid():
            don_data = donation.cleaned_data
            request.session['don_data'] = don_data
            request.session['camp_id'] = campana_id

            return redirect(reverse("insertCard"))
        else:
            donation.data = donation.data.copy
    else:
        donation = RegisterDonationForm()
    return render(request, 'donations/make_donation.html', {'form': donation})

def ViewMyDonations(request):
    donaciones=  list(Donacion.objects.filter(usuario=request.user))
    return render(request, "donations/donations.html", {"list_donations" : donaciones})

def AllDonations(request):
    donaciones=  list(Donacion.objects.order_by('campana__name'))
    return render(request, "donations/donations.html", {"list_donations" : donaciones})

def CampaignDonations(request, campana_id):
    donaciones=  list(Donacion.objects.filter(id=campana_id))
    return render(request, "donations/donations.html", {"list_donations" : donaciones}) 
