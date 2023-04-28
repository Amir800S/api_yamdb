from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import validate_regex_username, validate_username
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категории."""

    class Meta:
        exclude = ('id', )
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для жанров."""

    class Meta:
        exclude = ('id', )
        lookup_field = 'slug'
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET-запросе."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = ('__all__', )


class TitleWriteSerializer(TitleReadSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""

    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    def validate(self, data):
        if 'year' in data.keys():
            if data.get('year') > timezone.now().year:
                raise serializers.ValidationError(
                    'Год не может быть больше текущего!'
                )
        return data

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class AdminSerializer(serializers.ModelSerializer):
    """Сериалайзер для админа: Все поля редактируемы."""
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGHT,
        required=True,
        validators=[
            validate_regex_username,
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ])
    email = serializers.EmailField(
        required=True,
        max_length=settings.EMAIL_MAX_LENGHT),

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        constraints = [
            UniqueConstraint(fields=[
                'username',
                'email',
            ],
                name='Проверка уникальности email и username')
        ]


class UserSerializer(AdminSerializer):
    """Сериалайзер простого юзера: Невозможно поменять роль."""

    class Meta(AdminSerializer.Meta):
        read_only_fields = ('role',)


class TokenConfirmationSerializer(serializers.Serializer):
    """Сериалайзер токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class RegistrationSerializer(serializers.Serializer):
    """Сериалайзер для регистрации пользователя."""
    email = serializers.EmailField(required=True,
                                   max_length=settings.EMAIL_MAX_LENGHT,
                                   )
    username = serializers.CharField(required=True,
                                     max_length=settings.USERNAME_MAX_LENGHT,
                                     validators=(
                                         validate_username,
                                         validate_regex_username))

    class Meta:
        fields = (
            'username',
            'email',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'author', 'review', 'pub_date']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all(),
        required=False
    )

    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=None
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'author', 'title', 'pub_date']

    def validate(self, data):
        if self.context.get('view').action == 'create':
            request = self.context.get('request')
            title = get_object_or_404(
                Title,
                id=int(self.context.get('view').kwargs.get('title_id'))
            )
            if request and hasattr(request, 'user'):
                user = request.user
            if Review.objects.filter(author=user, title=title).exists():
                raise ValidationError(
                    {'Вы уже оставили отзыв на это произведение.'}
                )
        return data
