from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, views
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import RedirectView
from OMDApp.forms.accounts_form import LoginForm, RegisterForm


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
            request.session['email'] = user.email
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect(reverse("register"))
        else:
            messages.error(self.request, 'Contraseña incorrecta')
            return redirect(reverse("login"))

class LogOut(LoginRequiredMixin, RedirectView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        logout(request)
        self.pattern_name="login"
        return super().get(request, *args, **kwargs)

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
            email = form.cleaned_data['email']
            messages.success(request, f'Registro exitoso. Por favor, dirígase a {email} para activar su cuenta y completar el registro.')
            return redirect(reverse("landing"))
        messages.error(request, 'Registro fallido. Información inválida')
        return redirect(reverse("register"))
    form = RegisterForm
    return render(request, "accounts/register.html", {'register_form':form})