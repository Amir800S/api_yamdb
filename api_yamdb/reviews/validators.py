from django.utils import timezone

from django.core.exceptions import ValidationError


def valid_year(value):
    if value > timezone.now().year:
        raise ValidationError('Год выпуска не может быть больше текущего.')
