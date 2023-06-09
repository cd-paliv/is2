from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from OMDApp.models import Campana,Donacion
from django.contrib.auth.decorators import login_required
from OMDApp.forms.donations_form import RegisterDonationForm,RegisterCardForm, RegisterDonationEventsForm
from OMDApp.decorators import email_verification_required
from django.views.decorators.cache import cache_control

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RegisterEvent(request):
    if request.method == 'POST':
        form = RegisterDonationEventsForm(request.POST,request.FILES)
        if form.is_valid():
            camp = form.save(commit=False)
            camp.name = camp.name.title()
            camp.save()
            messages.success(request, 'Registro de Campaña exitoso')
            return redirect(reverse("home"))
        else:
            form.data = form.data.copy()
    else:
        form = RegisterDonationEventsForm()
    return render(request, 'donations/create_donation.html', {'form': form})

def ViewCampaigns(request):
    campanas = list(Campana.objects.order_by('name'))
    return render(request, "donations/view_donations.html", {"view_donations" : campanas})


@cache_control(max_age=3600, no_store=True)
def InsertCardView(request):
    if request.method == 'POST':
        form = RegisterCardForm(request.POST,request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            messages.success(request,'Donacion Realizada')
            return redirect(reverse("home"))
        else:
            form.data = form.data.copy()
    else:
        form = RegisterCardForm()
    return render(request, 'donations/payment.html', {'form': form})

@cache_control(max_age=3600, no_store=True)
def RegisterDonation(request, campana_id):
    if  request.method == 'POST':
        donation = RegisterDonationForm(request.POST,request.FILES)
        if donation.is_valid():
            don = donation.save(commit=False)
            don.campana= Campana.objects.get(id=campana_id)
            don.name = don.name.capitalize()
            don.message = don.message.capitalize()
            don.save()
            return redirect(reverse("insertCard"))
        else:
            donation.data = donation.data.copy
    else:
        donation = RegisterDonationForm()
    return render(request, 'donations/make_donation.html', {'form': donation})

def ViewMyDonations(request):
    donaciones=  list(Donacion.objects.order_by('name'))
    return render(request, "donations/donations.html", {"list_donations" : donaciones})

def AllDonations(request):
    donaciones=  list(Campana.objects.order_by('name'))
    return render(request, "donations/donations.html", {"list_donations" : donaciones}) 
