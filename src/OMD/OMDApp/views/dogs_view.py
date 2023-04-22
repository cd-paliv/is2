from django.views.generic import ListView
from datetime import date
from dateutil.relativedelta import relativedelta
from OMDApp.models import Perro
from django.contrib.auth.mixins import LoginRequiredMixin

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
                'name': dog.name,
                'breed': dog.breed,
                'photo': dog.photo or None,
                'age': calculate_age(dog.birthdate),
            })
        context['dog_list'] = dog_list
        context['one_dog'] = len(dog_list) == 1
        return context

def calculate_age(birthDate):
    today = date.today()
    age = relativedelta(today, birthDate)
    if age.years > 0:
        return f"{age.years} años"
    elif age.months > 0:
        return f"{age.months} meses"
    else:
        return f"{age.days} días"