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
    regex = re.compile(r'^[\w.@+-]+$')
    regex_matches = re.search(regex, value)
    if not regex_matches:
        forbidden_symbols = re.sub(regex, '', value)
        raise ValidationError(
            f'Некорректный символ для никнейма: {forbidden_symbols}'
            f' Только буквы, цифры и @/./+/-/_'
        )
    return value
