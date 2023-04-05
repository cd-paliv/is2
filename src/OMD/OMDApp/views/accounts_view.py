from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, views
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from OMDApp.forms.accounts_form import LoginForm, RegisterForm, RegisterDogForm


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
            return redirect(reverse("register"))
        else:
            messages.error(self.request, 'Contraseña incorrecta')
            return redirect(reverse("login"))

@login_required
def LogOut(request):
    logout(request)
    return redirect('home')

def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            actual_password = get_user_model().objects.make_random_password(length=20)
            user.password = make_password(actual_password)
            user.save()
            subject = 'Activa tu cuenta en OhMyDog'
            message = render_to_string('accounts/account_activation_email.html', { 'user': user, 'password': actual_password })
            user.email_user(subject, message)
            return redirect(reverse("registerDog", kwargs={"owner_id" : user.id}))
        messages.error(request, 'Registro fallido. Información inválida')
        return redirect(reverse("register"))
    form = RegisterForm
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':False})

def RegisterDogView(request, owner_id):
    if request.method == "POST":
        form = RegisterDogForm(request.POST)
        if form.is_valid():
            dog = form.save(commit=False)
            owner = get_user_model().objects.get(id=owner_id)
            dog.owner = owner
            dog.save()
            messages.success(request, f'Registro exitoso. Por favor, dirígase a {owner.email} para activar su cuenta y completar el registro.')
            return redirect(reverse("home"))
        messages.error(request, 'Registro fallido. Información inválida')
        return redirect(reverse("registerDog", kwargs={"owner_id" : owner.id}))
    form = RegisterDogForm
    return render(request, "accounts/register.html", {'register_form':form, 'dog_register':True})
