from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, PermissionsMixin
from django.utils.translation import gettext as _
import json

# Create your models here.
# Accounts
class CustomUserAccountManager(BaseUserManager):
    def create_user(self, email, password, dni, first_name, last_name, birthdate, email_confirmed, **other_fields):
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
        user = self.model(email=email, password=password, dni=dni, first_name=first_name, last_name=last_name, birthdate=birthdate, email_confirmed=email_confirmed, is_active=True, **other_fields)
        
        if password is not None:
            user.save()
        else:
            user.set_unusable_password()
            user.save()

        return user

    def create_superuser(self, email, password, dni, first_name, last_name, birthdate, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        user =  self.create_user(email=email, password=password, dni=dni, first_name=first_name, last_name=last_name, birthdate=birthdate, **other_fields)
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

class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    dni = models.IntegerField(unique=True)
    birthdate = models.DateField()
    photo = models.TextField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to="accounts/", default="default.png")

    class Meta:
        permissions = [
            ("is_client", "Correspondiente al rol de Cliente en la documentación"),
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
            ("is_vet", "Correspondiente al rol de Veterinario en la documentación"),
        ]

    def __str__(self):
        return f"{self.user}"

class Perro(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1) # F ^ M
    observations = models.TextField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    weight = models.FloatField(default=0.01)
    castrated = models.BooleanField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="dogs/", default="default.png")
    
    REQUIRED_FIELDS = ["name", "breed", "color", "birthdate"]

class PPEA(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    state = models.CharField(max_length=1)
    success = models.BooleanField(default=False)
    birthdate = models.DateField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)
    disappeared_date = models.DateField(blank=True, null=True)
    zone = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="ppea/", default="default.png")

    REQUIRED_FIELDS = ["name", "breed", "color", "zone"]

class Turno(models.Model):
    state = models.CharField(max_length=10, default="S") # solicited ^ accepted ^ rejected ^ finished
    type = models.CharField(max_length=15) # emergency ^ castration ^ turn ^ vacunation a ^ vacunation b
    hour = models.CharField(max_length=50)
    date = models.DateField()
    motive = models.TextField()
    observations = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    solicited_by = models.ForeignKey(Perro, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(Veterinario, on_delete=models.CASCADE, blank=True, null=True)
    finalized_at = models.DateField(blank=True, null=True)
    urgency_turns = models.TextField(blank=True, null=True)

    REQUIRED_FIELDS = ["type", "hour", "date", "motive"]

    def add_to_health_book(self):
        Libreta.objects.create(dog=self.solicited_by, finalized=self)

    def add_to_clinic_history(self):
        Historial.objects.create(dog=self.solicited_by, finalized=self)

class Libreta(models.Model):
    dog = models.ForeignKey(Perro, on_delete=models.CASCADE)
    finalized = models.ForeignKey(Turno, on_delete=models.CASCADE)

class Historial(models.Model):
    dog = models.ForeignKey(Perro, on_delete=models.CASCADE)
    finalized = models.ForeignKey(Turno, on_delete=models.CASCADE)

class UserAdoption(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dog = models.ForeignKey(PPEA, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Campana(models.Model):
    state = models.CharField(max_length=1, default='V') # vigente(valid) ^ finalizada
    name = models.CharField(max_length=50)
    estimated_amount = models.FloatField(max_length=10, blank=True, null=True)
    colected_amount = models.FloatField(max_length=10, default=0)
    date_in = models.DateField()
    date_out = models.DateField()

class Donacion(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(_('email address') )
    amount = models.FloatField(max_length=10, blank=True, null=True)
    message = models.CharField(blank=True,null=True, max_length=50)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
class Tarjeta(models.Model):
    holder = models.CharField(max_length=50)
    number = models.IntegerField()
    security_number = models.IntegerField()
    expiration = models.DateField()
    from_donation = models.OneToOneField(Donacion, on_delete=models.CASCADE, blank=True, null=True) 

class Servicio(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    service = models.CharField(max_length=1) # p ^ c
    zone = models.CharField(max_length=4)
    phone = models.IntegerField()