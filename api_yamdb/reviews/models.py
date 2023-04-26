from api.validators import validate_regex_username
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import valid_year


class BaseModel(models.Model):
    """Абстрактный родительский класс для моделей категория и жанр."""
    name = models.CharField(max_length=settings.TEXT_LENGTH,
                            unique=True,
                            blank=False,
                            verbose_name='имя')
    slug = models.SlugField(max_length=settings.SLUG_LENGTH,
                            unique=True,
                            blank=False,
                            verbose_name='slug')

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'Базовая модель'
        verbose_name_plural = 'Базовые модели'

    def __str__(self):
        return self.name


class Category(BaseModel):
    """Модель категория."""

    class Meta(BaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    """Модель жанр."""

    class Meta(BaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Название произведения',)
    year = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Год произведения',
        db_index=True,
        validators=(valid_year,))
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения',)
    genre = models.ManyToManyField(
        Genre,
        blank=False,
        verbose_name='Жанр произведения',)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Вспомогательная таблица многое-ко-многим - произведения и жанры."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title}-{self.genre}'


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        'Никнейм',
        max_length=150,
        null=False,
        blank=False,
        unique=True,
        validators=(validate_regex_username, )
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        null=False,
        unique=True,
        blank=False,
    )
    role = models.CharField(
        'Статус пользователя',
        max_length=15,
        choices=settings.USER_ROLE_CHOICES,
        default=settings.USER,
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
    confirmation_code = models.CharField(
        max_length=255,
        default='not defined yet',
        blank=True
    )

    def __str__(self):
        return 'Пользователь - {}'.format(self.username)

    class Meta:
        verbose_name_plural = 'Пользователи'
