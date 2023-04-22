from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, views
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from OMDApp.forms.accounts_form import LoginForm, RegisterForm, RegisterDogForm, UserEditForm


# Create your views here.
class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    def post(self, request, *args, **kwargs):
        instance_form = self.get_form(form_class=self.authentication_form)
        instance_form.is_valid()
        email = instance_form.cleaned_data['username']
        
        try:
            user = get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(self.request, 'El email no se encuentra registrado.')
            return redirect(reverse("login"))

        password = instance_form.cleaned_data['password']
        if check_password(password, user.password):
            if not user.is_active:
                user.is_active = True
                user.save()
            request.session['email'] = user.email
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect(reverse("home"))
        else:
            messages.error(self.request, 'Contraseña incorrecta')
            return redirect(reverse("login"))

@login_required
def LogOut(request):
    logout(request)
    return redirect(reverse("home"))

@login_required
def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.first_name = user.first_name.capitalize()
            user.last_name = user.last_name.capitalize()
            actual_password = get_user_model().objects.make_random_password(length=20)
            user.password = make_password(actual_password)
            
            user.save()
            client_perm = Permission.objects.get(codename='is_client')
            user.user_permissions.add(client_perm)
            
            request.session['message'] = render_to_string('accounts/account_activation_email.html', { 'user': user, 'password': actual_password })
            return redirect(reverse("registerDog", kwargs={"owner_id" : user.id}))
        elif form.errors:
            error_message = form.errors.as_data().get(list(form.errors.as_data().keys())[0])[0].message
            messages.error(request, error_message)
        return redirect(reverse("register"))
    form = RegisterForm
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':False})

@login_required
def RegisterDogView(request, owner_id):
    if request.method == "POST":
        form = RegisterDogForm(request.POST)
        if form.is_valid():
            dog = form.save(commit=False)
            owner = get_user_model().objects.get(id=owner_id)
            dog.owner = owner
            dog.save()

            subject = 'Activa tu cuenta en OhMyDog'
            owner.email_user(subject, request.session.get('message'))

            messages.success(request, f'Registro exitoso. Por favor, dirígase a {owner.email} para activar su cuenta y completar el registro.')
            return redirect(reverse("home"))
        elif form.errors:
            error_message = form.errors.as_data().get(list(form.errors.as_data().keys())[0])[0].message
            messages.error(request, error_message)
        return redirect(reverse("registerDog", kwargs={"owner_id" : owner.id}))
    form = RegisterDogForm
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':True})

@login_required
def RegisterSingleDogView(request):
    if request.method == "POST":
        form = RegisterDogForm(request.POST)
        if form.is_valid():
            dog = form.save(commit=False)
            owner = get_user_model().objects.get(email=request.session['email'])
            dog.owner = owner
            dog.save()

            messages.success(request, f'Registro de perro exitoso.')
            return redirect(reverse("home"))
        elif form.errors:
            error_message = form.errors.as_data().get(list(form.errors.as_data().keys())[0])[0].message
            messages.error(request, error_message)
        return redirect(reverse("registerSingleDog"))
    form = RegisterDogForm
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':True})

@login_required
def ProfileView(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'accounts/edit_profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = UserEditForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            # Update user object with new data
            if form.cleaned_data.get('first_name'):
                user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data.get('last_name'):
                user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data.get('birthdate'):
                user.birthdate = form.cleaned_data['birthdate']
            user.save()
            # Redirect to a success page or display a success message
            messages.success(request, f'Datos modificados.')
            return redirect(reverse("profile"))
        return render(request, self.template_name, {'form': form})
