from django.contrib import admin
from .models import CustomUser, Perro

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Perro)