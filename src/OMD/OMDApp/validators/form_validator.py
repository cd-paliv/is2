

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
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
            raise ValidationError(_(f"El campo debe ser una fecha válida."))

    def get_help_text(self):
        return _("Este campo debe ser una fecha válida.")

class UserAgeValidator:
    def __call__(self, field):
        today = date.today()
        min_date = today - timedelta(days=365 * 18)  # hace 18 años
        max_date = date(1900, 1, 1)  # 1ero de Enero, 1900

        if field <= max_date or field >= min_date:
            raise ValidationError(_(f"El campo debe ser una fecha válida."))

    def get_help_text(self):
        return _("Este campo debe ser una fecha válida, 1900-2005.")
    
class ExistsEmailValidator:
    def __call__(self, email):
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(_(f"El email ya se encuentra registrado."))

    def get_help_text(self):
        return _("El email ya se encuentra registrado.")
    
class ExistsDNIValidator:
    def __call__(self, dni):
        if get_user_model().objects.filter(email=dni).exists():
            raise ValidationError(_(f"El DNI ya se encuentra registrado."))

    def get_help_text(self):
        return _("El DNI ya se encuentra registrado.")