from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=15, null=False)
    apellido = models.CharField(max_length=20, null=False)
    fnacimiento = models.DateField(null=False)
    DNI = models.IntegerField(null=False)
    email = models.EmailField(max_length=128, unique=True, null=False)
    #perros = models.OneToOneField(User, on_delete=models.CASCADE)

class Perro(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    raza = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=10, null=False)
    fnacimiento = models.DateField(null=False)
    observaciones = models.TextField(null=False)
    foto = models.TextField(null=True)
    dueno = models.ForeignKey(to=Cliente, on_delete=models.CASCADE, null=True, blank=True)