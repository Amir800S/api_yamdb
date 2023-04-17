from django.db import models


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        blank=False,
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        blank=False,
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        blank=False,
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        blank=False,
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name
