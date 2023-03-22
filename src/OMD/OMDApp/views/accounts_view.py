from django.shortcuts import render, redirect
from OMDApp.forms.accounts_form import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import views, get_user_model, login, logout
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from OMDApp.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http.response import HttpResponseBase

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
        
        confirmed = getattr(user, 'email_confirmed')
        if not confirmed:
            messages.error(request, 'El email no se encuentra confirmado. Dirígase a su correo para finalizar el registro.')
            return redirect(reverse("register"))

        password = instance_form.cleaned_data['password']
        if check_password(password, user.password):
            request.session['email'] = user.email
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
            user.save()
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta en OhMyDog'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            email = form.cleaned_data['email']
            messages.success(request, f'Registro exitoso. Por favor, dirígase a {email} para activar su cuenta y completar el registro.')
            return redirect(reverse("register"))
        messages.error(request, 'Registro fallido. Información inválida')
        return render(request, "accounts/register.html", {'register_form':form})
    form = RegisterForm
    return render(request, "accounts/register.html", {'register_form':form})

def ConfirmRegisterView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if (user is not None) and (account_activation_token.check_token(user, token)):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Registro confirmado')
        return redirect(reverse("login"))
    else:
        messages.error(request, 'Confirmación de registro fallida. Intente de vuelta.')
        return redirect(reverse("register"))