from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.models import Title, User

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