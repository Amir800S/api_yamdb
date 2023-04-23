from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import valid_year
from api.validators import validate_username, validate_regex_username


class Category(models.Model):
    name = models.CharField(
        blank=False,
        max_length=256,
        unique=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        blank=False,
        max_length=50,
        unique=True,
        verbose_name='Slug категории',
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        blank=False,
        max_length=256,
        unique=True,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        blank=False,
        max_length=50,
        unique=True,
        verbose_name='Slug жанра',
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Название произведения',)
    year = models.IntegerField(
        blank=False,
        verbose_name='Год произведения',
        validators=(valid_year,))
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения',)
    genre = models.ForeignKey(
        Genre,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Жанр произведения',)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',)


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
            validate_regex_username),
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


class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ID произведения',
    )
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Текст отзыва',
    )
    score = models.IntegerField(
        blank=False,
        null=False,
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:15]
