from datetime import datetime
from django.core.exceptions import ValidationError


def valid_year(value):
    if value > datetime.date.today().year:
        raise ValidationError('Год выпуска не может быть больше текущего.')
