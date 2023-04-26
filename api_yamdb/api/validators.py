import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """В качестве ника запрещает использовать 'me'."""
    if value == 'me':
        raise ValidationError(
            'Запрещенное имя пользователя - "me".'
        )
    return value


def validate_regex_username(value):
    """Проверка на отсутсвие запрещенных символов."""
    if not re.search(r'^[\w.@+-]+$', value):
        raise ValidationError(
            'Некорректный никнейм: Только буквы, цифры и @/./+/-/_'
        )
    return value
