from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_control
from OMDApp.decorators import email_verification_required
from django.template.loader import render_to_string
from OMDApp.forms.services_form import RegisterServiceForm, ContactServiceForm
from OMDApp.models import Servicio
from django.core.mail import send_mail
from OMDApp.views.helpers import zone_mapping

# Create your views here.
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RegisterService(request, type_s):
    if request.method == "POST":
        form = RegisterServiceForm(request.POST)
        if form.is_valid():
            serv = form.save(commit=False)
            serv.service = 'C' if type_s == 'C' else 'P'
            serv.save()

            messages.success(request, "Nuevo servicio registrado")
            if type_s == 'C':
                return redirect(reverse("viewCuidadores"))
            else:
                return redirect(reverse("viewPaseadores"))
        else:
            form.data = form.data.copy()
    else:
        form = RegisterServiceForm()
    return render(request, "services/register.html", {'form': form})

def ViewCuidadores(request):
    cuidadores = Servicio.objects.filter(service='C')
    return render(request, "services/service_list.html", {'services': cuidadores, 'type': 'C',
                                                          'zone_mapping': zone_mapping()})

def ViewPaseadores(request):
    paseadores = Servicio.objects.filter(service='P')
    return render(request, "services/service_list.html", {'services': paseadores, 'type': 'P',
                                                          'zone_mapping': zone_mapping()})

def ContactService(request, serv_id):
    if request.method == "POST":
        form = ContactServiceForm(request.POST)
        if form.is_valid():
            contact_data = form.cleaned_data
            service = Servicio.objects.get(id=serv_id)
            service_type = "Cuidador" if service.service == 'C' else "Paseador"

            message = render_to_string("services/contact_email.html", {'type': service_type, 'data': contact_data})
            send_mail("Solicitud de contacto", message, 'noreply.omd@gmail.com', [service.email])
            
            if service.service == 'C':
                return redirect(reverse("viewCuidadores"))
            else:
                return redirect(reverse("viewPaseadores"))
        else:
            form.data = form.data.copy()
    else:
        form = ContactServiceForm()
    return render(request, "services/contact.html", {'form': form})