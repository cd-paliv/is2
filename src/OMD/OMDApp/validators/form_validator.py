

from typing import Any
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta, timezone
from django.contrib.auth import get_user_model

class EmptyFieldValidator:
    def __call__(self, field):
        if not field:
            raise ValidationError(_(f"El campo es obligatorio."))

    def get_help_text(self, field):
        return _(f"Este campo es obligatorio.")

class NoNumbersFieldValidator:
    def __call__(self, field):
        if any(char.isdigit() for char in str(field)):
            raise ValidationError(_(f"El campo no puede contener números."))

    def get_help_text(self, field):
        return _(f"Este campo no puede contener números.")
    
class NumbersFieldValidator:
    def __call__(self, field):
        if not any(char.isdigit() for char in str(field)):
            raise ValidationError(_(f"El campo sólo puede contener números."))

    def get_help_text(self, field):
        return _(f"Este campo sólo puede contener números.")

class FloatFieldValidator:
    def __call__(self, field):
        try:
            field = float(field)
        except ValueError:
            raise ValidationError('El valor ingresado debe ser un número válido.')  # Display a validation error
        return field

    def get_help_text(self):
        return _(f"El valor ingresado debe ser un número válido.")
    
class GreaterThanZeroValidator:
    def __call__(self, field):
        if field <= 0:
            raise ValidationError(_(f"El campo debe ser mayor que cero."))

    def get_help_text(self):
        return _("Este campo debe ser mayor que cero.")
    
class DogAgeValidator:
    def __call__(self, field):
        min_date = date.today()
        max_date = date(1990, 1, 1)  # 1ero de Enero, 1990

        if field <= max_date or field >= min_date:
            raise ValidationError(_(f"El campo debe ser una fecha de nacimiento válida."))

    def get_help_text(self):
        return _("Este campo debe ser una fecha válida.")

class UserAgeValidator:
    def __call__(self, field):
        today = date.today()
        min_date = today - timedelta(days=365 * 18)  # hace 18 años
        max_date = date(1900, 1, 1)  # 1ero de Enero, 1900

        if field <= max_date or field >= min_date:
            raise ValidationError(_(f"El campo debe ser una fecha de nacimiento válida."))

    def get_help_text(self):
        return _("Este campo debe ser una fecha válida, 1900-2005.")

class TurnDateBetweenValidator:
    def __call__(self, field):
        tomorrow = date.today() + timedelta(days=1)
        end_of_year = date(2023, 12, 31)

        if field < tomorrow or field > end_of_year:
            raise ValidationError(_(f"El campo debe ser una fecha válida en este año"))

    def get_help_text(self):
        return _("Este campo debe ser una fecha válida, Mañana-31/12/2023.")

class TurnDateTodayValidator:
    def __call__(self, field):
        today = date.today()

        if field == today:
            raise ValidationError(_(f"No se puede sacar turno en el dia"))

    def get_help_text(self):
        return _("No se puede sacar turno en el dia.")

    
class ExistsEmailValidator:
    def __call__(self, email):
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(_(f"El email ya se encuentra registrado."))

    def get_help_text(self):
        return _("El email ya se encuentra registrado.")
    
class ExistsDNIValidator:
    def __call__(self, dni):
        if get_user_model().objects.filter(dni=dni).exists():
            raise ValidationError(_(f"El DNI ya se encuentra registrado."))

    def get_help_text(self):
        return _("El DNI ya se encuentra registrado.")
    
class ImageFileTypeValidator:
    def __init__(self, allowed_types=('image/jpeg', 'image/png')):
        self.allowed_types = allowed_types

    def __call__(self, value):
        if value.content_type not in self.allowed_types:
            raise ValidationError("Sólo se permiten archivos JPG, JPEG o PNG.")
    
    def get_help_text(self):
        return _("Sólo se permiten archivos JPG, JPEG o PNG.")

from OMDApp.models import Tarjeta
    
class CardNumberValidation:
    def __call__(self, field):
        if not Tarjeta.objects.filter(number=field).exists():
            raise ValidationError(_(f"El número de tarjeta ingresado no coincide con una tarjeta existente"))

    def get_help_text(self, field):
        return _(f"El número de tarjeta ingresado no coincide con una tarjeta existente")
    
class CardSecurityNumberValidation:
    def __call__(self, field):
        if not Tarjeta.objects.filter(security_number=field).exists():
            raise ValidationError(_(f"El código de seguridad ingresado es incorrecto"))

    def get_help_text(self, field):
        return _(f"El código de seguridad ingresado es incorrecto")

class CardHolderValidation:
    def __call__(self, field):
        if not Tarjeta.objects.filter(holder__iexact=field).exists():
            raise ValidationError(_(f"El titular de la tarjeta ingresado es incorrecto"))

    def get_help_text(self, field):
        return _(f"El titular de la tarjeta ingresado es incorrecto")
    
class CardValidExpirationValidation:
    def __call__(self, field):
        if field <= date.today():
            raise ValidationError(_(f"La tarjeta ingresada está vencida"))

    def get_help_text(self, field):
        return _(f"La tarjeta ingresada está vencida")

class CardExpirationValidation:
    def __call__(self, field):
        if not Tarjeta.objects.filter(expiration=field).exists():
            raise ValidationError(_(f"La fecha de vencimiento de la tarjeta no coincide con la ingresada"))

    def get_help_text(self, field):
        return _(f"La fecha de vencimiento de la tarjeta no coincide con la ingresada")