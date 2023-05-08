import functools
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect



def email_verification_required(view_func, verification_url="editpassword"):
    """
        this decorator restricts users who have not verified their emails
        from accessing the view function passed as it argument and
        redirect the user to page where their account can be activated
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.email_confirmed:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Por favor, modifique la contraseña para acceder al sitio.')
        return redirect(reverse("editPassword"))
    return wrapper