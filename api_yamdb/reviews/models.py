from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import validate_username, validate_regex_username


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        'Никнейм',
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        validators=(
            validate_username,
            validate_regex_username ),
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        null=False,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    bio = models.CharField(
        'Биография',
        max_length=200,
        blank=True
    )
    role = models.CharField(
        'Статус пользователя',
        max_length=15,
        choices=settings.USER_ROLE_CHOICES,
        default=settings.USER,
    )
    confirmation_code = models.CharField(
        max_length=255,
        default='not defined yet'
    )

    def __str__(self):
        return 'Пользователь - {}'.format(self.username)
    class Meta:
        verbose_name_plural = 'Пользователи'