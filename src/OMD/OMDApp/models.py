from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.utils.translation import gettext as _

# Create your models here.
# Accounts
class CustomUserAccountManager(BaseUserManager):
    def create_superuser(self, email, password, dni, first_name, last_name, birthdate, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        user.user_permissions.set([Permission.objects.get(codename="Veterinario")])
        user.user_permissions.set([Permission.objects.get(codename="Cliente")])
        
        user = self.create_user(email=email, password=password, dni=dni, first_name=first_name, last_name=last_name, birthdate=birthdate, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_vet(self, email, password, dni, first_name, last_name, birthdate, **other_fields):
        extra_fields = {}
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False

        user = self.create_user(email=email, password=password, dni=dni, first_name=first_name, last_name=last_name, birthdate=birthdate, **other_fields)
        user.user_permissions.set([Permission.objects.get(codename="Veterinario")])
        user.save()
        return user

    def create_user(self, email, password, dni, first_name, last_name, birthdate, **other_fields):
        if not dni:
            raise ValueError("El DNI es obligatorio")
        if not first_name:
            raise ValueError("El nombre es obligatorio")
        if not last_name:
            raise ValueError("El apellido es obligatorio")
        if not birthdate:
            raise ValueError("La fecha de nacimiento es obligatoria")
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, dni=dni, first_name=first_name, last_name=last_name, birthdate=birthdate, **other_fields)
        user.user_permissions.set([Permission.objects.get(codename="Cliente")])
        if password is not None:
            user.save()
        else:
            user.set_unusable_password()
            user.save()

        return user

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    dni = models.IntegerField(unique=True)
    birthdate = models.DateField()
    photo = models.TextField(blank=True, null=True)

    class Meta:
        permissions = [
            ("Cliente", "Correspondiente al rol de Cliente en la documentación"),
        ]

    objects = CustomUserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "dni", "birthdate", "password"]

    def __str__(self):
        return self.email

class Veterinario(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("Veterinario", "Correspondiente al rol de Veterinario en la documentación"),
        ]

    def __str__(self):
        return f"{self.user}"

class Perro(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    birthdate = models.DateField()
    observations = models.TextField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ["name", "breed", "color", "birthdate"]