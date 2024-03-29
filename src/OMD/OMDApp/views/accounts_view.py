from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views import View
from OMDApp.models import Perro
from django.db.models import Q
from OMDApp.decorators import email_verification_required
from django.contrib.auth import authenticate
from OMDApp.forms.accounts_form import (EditPasswordForm, LoginForm,
                                        RegisterDogForm, RegisterForm,
                                        UserEditForm)


logged_decorators = [login_required, email_verification_required, cache_control(max_age=3600, no_store=True)]

# Create your views here.
class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            messages.error(self.request, 'Email y/o contraseña no válidos.')
            return HttpResponseRedirect(reverse("login"))
        
        if check_password(password, user.password):
            request.session['email'] = email
            login(request, user)

            if not user.email_confirmed:
                messages.success(request, 'Inicio de sesión exitoso. Por favor, modifique la contraseña para acceder al sitio.')
                return HttpResponseRedirect(reverse("editPassword"))
            
            messages.success(request, 'Inicio de sesión exitoso')
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(self.request, 'Email y/o contraseña no válidos.')
            return HttpResponseRedirect(reverse("login"))

@login_required(login_url='/login/')
def LogOut(request):
    logout(request)
    return redirect(reverse("home"))

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RegisterView(request, urgency=False):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():

            user_data = form.cleaned_data
            user_data['birthdate'] = user_data['birthdate'].isoformat()
            request.session['user_data'] = user_data
            
            if bool(urgency):
                return redirect(reverse("registerDog", kwargs={'urgency': 1}))
            return redirect(reverse("registerDog"))
        else:
            form.data = form.data.copy()
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':False})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RegisterDogView(request, urgency=False):
    if request.method == "POST":
        form = RegisterDogForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user
            user_data = request.session.get('user_data')
            user = get_user_model().objects.create(**user_data)
            del request.session['user_data']

            # Change data & create password
            user.first_name = user.first_name.capitalize()
            user.last_name = user.last_name.capitalize()
            user.is_active = True
            actual_password = get_user_model().objects.make_random_password(length=20)
            user.password = make_password(actual_password)

            user.save()
            client_perm = Permission.objects.get(codename='is_client')
            user.user_permissions.add(client_perm)
            message = render_to_string('accounts/account_activation_email.html', { 'user': user, 'password': actual_password })

            dog = form.save(commit=False)
            dog.name = dog.name.capitalize()
            dog.breed = dog.breed.capitalize()
            dog.color = dog.color.capitalize()
            dog.owner = user
            dog.save()

            if bool(urgency):
                return redirect(reverse("generateUrgency", kwargs={'dog_id': dog.id}))

            subject = 'Activa tu cuenta en OhMyDog'
            user.email_user(subject, message)

            messages.success(request, f'Registro exitoso. Por favor, diríjase a {user.email} para activar su cuenta y completar el registro.')
            return redirect(reverse("home"))
    else:
        form = RegisterDogForm
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':True})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def RegisterSingleDogView(request):
    if request.method == "POST":
        form = RegisterDogForm(request.POST, request.FILES)
        if form.is_valid():
            owner = get_user_model().objects.get(email=request.session['email'])
            name = form.cleaned_data['name'].capitalize()
            breed = form.cleaned_data['breed'].capitalize()
            color = form.cleaned_data['color'].capitalize()
            birthdate = form.cleaned_data['birthdate']
            if Perro.objects.filter(name=name, breed=breed, color=color, birthdate=birthdate, owner=owner).exists():
                messages.error(request, 'El perro ya se encuentra registrado')
                return redirect(reverse("registerSingleDog"))
            
            dog = form.save(commit=False)
            dog.name = dog.name.capitalize()
            dog.breed = dog.breed.capitalize()
            dog.color = dog.color.capitalize()
            dog.owner = owner
            dog.save()

            messages.success(request, f'Registro de perro exitoso.')
            return redirect(reverse("home"))
    else:
        form = RegisterDogForm
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':True})


@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def ProfileView(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})

@method_decorator(logged_decorators, name='dispatch')
class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'accounts/edit_profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = UserEditForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Update user object with new data
            if form.cleaned_data.get('first_name'):
                user.first_name = form.cleaned_data['first_name'].capitalize()
            if form.cleaned_data.get('last_name'):
                user.last_name = form.cleaned_data['last_name'].capitalize()
            if form.cleaned_data.get('birthdate'):
                user.birthdate = form.cleaned_data['birthdate']
            if 'image' in request.FILES:
                user.image = request.FILES['image']
            user.save()
            messages.success(request, f'Datos modificados.')
            return redirect(reverse("profile"))
        return render(request, self.template_name, {'form': form})
        

class EditPasswordView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'accounts/edit_password.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = EditPasswordForm()
        return render(request, self.template_name, {'form': form, 'confirmed': user.email_confirmed})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = EditPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            if check_password(password, user.password):
                newPassword = form.cleaned_data['new_password']

                if newPassword != form.cleaned_data['repeat_new_password']:
                    messages.error(request, 'Las contraseñas no coinciden, por favor, intente de nuevo')
                    return redirect(reverse("editPassword"))
                
                if not user.email_confirmed:
                    get_user_model().objects.filter(id=user.id).update(password=make_password(newPassword), email_confirmed=True)
                else:
                    get_user_model().objects.filter(id=user.id).update(password=make_password(newPassword))
                user.refresh_from_db()

                request.session['email'] = user.email
                messages.success(request, 'Cambio de contraseña exitoso')
                return redirect(reverse("home"))
            else:
                messages.error(self.request, 'Contraseña actual incorrecta')
                return redirect(reverse("editPassword"))
        return render(request, self.template_name, {'form': form, 'confirmed': user.email_confirmed})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def UserListView(request):
    users = get_user_model().objects.all().exclude(Q(id=1) | Q(id=2) | Q(id=3))

    return render(request, "accounts/user_list.html", {'model_list': users, 'is_user': 1})

@login_required(login_url='/login/')
@email_verification_required
@cache_control(max_age=3600, no_store=True)
def UsersDogsListView(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    dogs = Perro.objects.filter(owner=user)

    return render(request, "accounts/user_list.html", {'model_list': dogs, 'is_user': 0})