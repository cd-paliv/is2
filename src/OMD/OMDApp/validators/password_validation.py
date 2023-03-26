import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MinimumLengthValidator:
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ("Tu contraseña debe contener al menos %(min_length)d caracteres."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return (
            "Tu contraseña debe contener al menos %(min_length)d caracteres."
            % {'min_length': self.min_length}
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("Tu contraseña debe contener al menos 1 caracter especial: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos 1 caracter especial: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )

class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("Tu contraseña debe contener al menos 1 dígito, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos 1 dígito, 0-9."
        )

class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Tu contraseña debe contener al menos 1 mayúscula, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos 1 mayúscula, A-Z."
        )