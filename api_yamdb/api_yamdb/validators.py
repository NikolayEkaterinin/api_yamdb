from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_username(value):
    if value == 'me':
        raise ValidationError("Ник не может содержать 'me'")

    pattern = r'^[a-zA-Z0-9.@+-_]+$'
    if not re.match(pattern, value):
        raise ValidationError("Недопустимые символы в нике")


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
