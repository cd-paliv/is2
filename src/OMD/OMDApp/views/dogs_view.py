from OMDApp.views.helpers import calculate_age
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views import View
from OMDApp.forms.dogs_form import RegisterAdoptionDogForm, AdoptionForm
from OMDApp.forms.accounts_form import RegisterDogForm
from OMDApp.decorators import email_verification_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from OMDApp.models import Perro, PPEA, UserAdoption, Libreta, Turno
from django.template.loader import render_to_string
from OMDApp.views.helpers import turn_hour_mapping, turn_type_mapping, turn_type_mapping_with_urgency
from django.db.models import Q


logged_decorators = [login_required, email_verification_required, cache_control(max_age=3600, no_store=True)]


# Create your views here
@method_decorator(logged_decorators, name='dispatch')
class DogListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Perro
    template_name = 'dogs/mis_perros.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dogs = Perro.objects.filter(owner=user)
        dog_list = []
        for dog in dogs:
            dog_list.append({
                'id' : dog.id,
                'name': dog.name,
                'breed': dog.breed,
                'image': dog.image.url if dog.image else None,
                'age': calculate_age(dog.birthdate),
            })
        context['dog_list'] = dog_list
        context['four_dogs'] = len(dog_list) <= 4
        return context
    
@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ProfileDogView(request, dog_id):
    request.session['actual_dog'] = dog_id
    dog = Perro.objects.get(id=dog_id)
    return render(request, 'dogs/profile.html', {'dog': dog})

@method_decorator(logged_decorators, name='dispatch')
class EditProfileDogView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'dogs/edit_profile.html'

    def get(self, request, *args, **kwargs):
        dog_id = request.session.get('actual_dog')
        dog = Perro.objects.get(id=dog_id)
        form = RegisterDogForm(instance=dog)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        dog_id = request.session.get('actual_dog')
        dog = Perro.objects.get(id=dog_id)
        form = RegisterDogForm(request.POST, instance=dog)
        if form.is_valid():
            # Update user object with new data
            if form.cleaned_data.get('name'):
                dog.name = form.cleaned_data['name'].capitalize()
            if form.cleaned_data.get('breed'):
                dog.breed = form.cleaned_data['breed'].capitalize()
            if form.cleaned_data.get('color'):
                dog.color = form.cleaned_data['color'].capitalize()
            if form.cleaned_data.get('birthdate'):
                dog.birthdate = form.cleaned_data['birthdate']
            if form.cleaned_data.get('observations'):
                dog.observations = form.cleaned_data['observations']
            if 'image' in request.FILES:
                dog.image = request.FILES['image']
            
            if Perro.objects.filter(name=dog.name, breed=dog.breed, color=dog.color, birthdate=dog.birthdate, owner=dog.owner).exists():
                messages.error(request, 'El perro ya se encuentra registrado')
                return redirect(reverse("my_dogs"))

            if Perro.objects.filter(name=dog.name, breed=dog.breed, color=dog.color, birthdate=dog.birthdate).exists():
                messages.error(request, 'El perro ya se encuentra registrado')
                return redirect(reverse("dog_edit_profile"))

            dog.save()
            messages.success(request, f'Datos modificados.')
            return redirect(reverse("dog_profile", kwargs={"dog_id" : dog.id}))
        return render(request, self.template_name, {'form': form, 'dog_id' : dog.id})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RegisterAdoptionDogView(request):
    if request.method == "POST":
        form = RegisterAdoptionDogForm(request.POST)
        if form.is_valid():
            dog = form.save(commit=False)
            if PPEA.objects.filter(name=dog.name, breed=dog.breed, color=dog.color, birthdate=dog.birthdate, state='A').exists():
                messages.error(request, 'El perro en adopción ya se encuentra registrado')
                return redirect(reverse("adoption_dog_list"))
            
            if PPEA.objects.filter(publisher=request.user, name=dog.name).exists():
                messages.error(request, 'Ya ha dado de alta un perro con el nombre ingresado')
                return redirect(reverse("adoption_dog_list"))

            dog.state = "A"
            dog.publisher = request.user
            dog.save()

            messages.success(request, f'Perro en adopción dado de alta.')
            return redirect(reverse("adoption_dog_list"))
        else:
            form.data = form.data.copy()
    else:
        form = RegisterAdoptionDogForm()
    return render(request, "dogs/adoption/register_adoption.html", {'form': form})

from django.db.models import F
@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AdoptionDogListView(request):
    dog_list = list(PPEA.objects.filter(state="A", success=False))
    adoption_list = []

    for dog in dog_list:
            adoption_list.append({
                'id' : dog.id,
                'name': dog.name,
                'breed': dog.breed,
                'color': dog.color,
                'publisher_id': dog.publisher.id,
                'age': calculate_age(dog.birthdate),
            })
    print(request.user.id)
    return render(request, "dogs/adoption/view_adoption.html", {'adoption_list': adoption_list, 'user_id': request.user.id,
                                                                't': 'all', 'c': 'asc', 'adoption': True})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AdoptionDogListFilteredView(request):
    type = request.GET.get('typeFilter')
    criteria = request.GET.get('criteriaFilter')
    if type == "all" and criteria == "desc":
        dog_list = list(PPEA.objects.filter(state="A", success=False).order_by(F('birthdate').desc()))
    elif type == "age":
        dog_list = list(PPEA.objects.filter(state="A", success=False).order_by(
            F('birthdate').asc() if criteria == "desc" else F('birthdate').desc()
        ))
    elif type == "breed":
        dog_list = list(PPEA.objects.filter(state="A", success=False).order_by(
            F('breed').asc() if criteria == "asc" else F('breed').desc()
        ))
    else:
        return redirect(reverse('adoption_dog_list'))
    
    adoption_list = []
    for dog in dog_list:
            adoption_list.append({
                'id' : dog.id,
                'name': dog.name,
                'breed': dog.breed,
                'color': dog.color,
                'publisher_id': dog.publisher.id,
                'age': calculate_age(dog.birthdate),
            })
    return render(request, "dogs/adoption/view_adoption.html", {'adoption_list': adoption_list, 'user_id': request.user.id,
                                                                't': type, 'c': criteria, 'adoption': True})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AdoptedDogListView(request):
    dog_list = list(PPEA.objects.filter(state="A", success=True))
    adoption_list = []

    for dog in dog_list:
            adoption_list.append({
                'id' : dog.id,
                'name': dog.name,
                'breed': dog.breed,
                'color': dog.color,
                'publisher_id': dog.publisher.id,
                'age': calculate_age(dog.birthdate),
            })
    print(request.user.id)
    return render(request, "dogs/adoption/view_adoption.html", {'adoption_list': adoption_list, 'adoption': False})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def AdoptionDog(request, dog_id):
    dog = PPEA.objects.get(id=dog_id)
    user = request.user
    if UserAdoption.objects.filter(user=user, dog=dog).exists():
        messages.error(request, 'Ya ha solicitado adoptar este perro. El dueño se comunicará a la brevedad.')
        return redirect(reverse('adoption_dog_list'))

    if request.method == "POST":
        form = AdoptionForm(request.POST)
        if form.is_valid():
            usr = { 
                'name' : form.cleaned_data['name'],
                'email' : form.cleaned_data['email'],
                'motive' : form.cleaned_data['motive']
            }
            message = render_to_string('dogs/adoption/request_adoption_email.html', { 'dog': dog, 'user': usr })
            dog.publisher.email_user("Solicitud de Adopcion", message)

            user_data = {
                'user' : user,
                'dog' : dog,
            }
            UserAdoption.objects.create(**user_data)

            messages.success(request, 'Solicitud de adopcion enviada')
            return redirect(reverse('adoption_dog_list'))
    else:
        user = request.user
        name = user.first_name + " " + user.last_name
        email = user.email
        form = AdoptionForm(initial={'name': name, 'email': email})

    return render(request, "dogs/adoption/request_adoption.html", {'form':form})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def SwitchAdoptedDogView(request, dog_id):
    dog = PPEA.objects.get(id=dog_id)
    dog.success = True
    dog.save()

    messages.success(request, 'Perro marcado como adoptado')
    return redirect(reverse('adoption_dog_list'))


from django.template.defaulttags import register
import json
@register.filter
def json_to_list(value):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []
    
@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def HealthBookDogView(request, dog_id):
    dog = Perro.objects.get(id=dog_id)
    vacunas = Turno.objects.filter(libreta__dog=dog).filter(Q(type='VA') | Q(type='VB'))
    #Libreta.objects.filter(dog=dog, finalized__type__in=['VA', 'VB']).select_related('finalized')
    operaciones = Turno.objects.filter(libreta__dog=dog).exclude(Q(type='VA') | Q(type='VB') | Q(type='T') | Q(type='U'))
    #Libreta.objects.filter(dog=dog).exclude(finalized__type__in=['VA', 'VB', 'T', 'U']).select_related('finalized')

    return render(request, "dogs/health_book.html", {"vacunas" : vacunas, 'operaciones':operaciones, 'dog': dog, 'dog_age': calculate_age(dog.birthdate),
                                                     'turn_type_mapping': turn_type_mapping(), 'turn_hour_mapping': turn_hour_mapping()})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ClinicHistoryDogView(request, dog_id):
    dog = Perro.objects.get(id=dog_id)
    #clinic_history_turns = list(Historial.objects.filter(dog=dog).select_related('finalized'))
    clinic_history_turns = Turno.objects.filter(historial__dog=dog).exclude(motive__icontains='realizada en urgencia')

    
    return render(request, "dogs/history_clinic.html", {"turns" : clinic_history_turns, 'name': dog.name, 'dog_id': dog.id,
                                                     'turn_type_mapping': turn_type_mapping_with_urgency(), 'turn_hour_mapping': turn_hour_mapping()})