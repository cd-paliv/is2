from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from yourapp.models import User # if you have a custom user


class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata', 'vet.json')
        # Fix the passwords of fixtures
        for user in get_user_model().objects.all():
            user.set_password(user.password)
            user.save()