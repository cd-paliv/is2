from django.core.management import BaseCommand, call_command
from OMDApp.models import Veterinario, Turno
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
# from yourapp.models import User # if you have a custom user


class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata', 'vet.json')
        # Set vet permissions
        vet_perm = Permission.objects.get(codename='is_vet')
        for vet in Veterinario.objects.all():
            vet.user.user_permissions.add(vet_perm)
        # Fix the passwords of fixtures and set client permissions
        client_perm = Permission.objects.get(codename='is_client')
        for user in get_user_model().objects.all():
            if user.email.startswith("user"):
                user.user_permissions.add(client_perm)
            user.set_password(user.password)
            user.save()

        for turn in Turno.objects.filter(state='F'):
            turn.add_to_clinic_history()
            turn.add_to_health_book()