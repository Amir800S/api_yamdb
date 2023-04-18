from django.db import models
from .validators import valid_year


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
