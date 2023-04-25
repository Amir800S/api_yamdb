from statistics import mean

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User
from .validators import validate_regex_username, validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категории."""

    class Meta:
        exclude = ('id', )
        lookup_field = "slug"
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для жанров."""

    class Meta:
        exclude = ('id', )
        lookup_field = "slug"
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET-запросе."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

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
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        reviews = Review.objects.filter(title_id=obj.id)
        scores = []
        for review in reviews:
            scores.append(review.score)
        if len(scores) > 0:
            return mean(scores)
        else:
            return None


class TitleWriteSerializer(TitleReadSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""

    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug',
                                            )


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


class TokenConfirmationSerializer(AdminSerializer):
    """Сериалайзер токена."""
    confirmation_code = serializers.CharField(required=True)

    class Meta(AdminSerializer.Meta):
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class RegistrationSerializer(AdminSerializer):
    """Сериалайзер для регистрации пользователя."""
    email = serializers.EmailField(required=True,
                                   max_length=settings.EMAIL_MAX_LENGHT,)
    username = serializers.CharField(required=True,
                                     max_length=settings.USERNAME_MAX_LENGHT,
                                     validators=(
                                         validate_username,
                                         validate_regex_username))

    class Meta(AdminSerializer.Meta):
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

    def validate_author(self, value):
        request = self.context.get("request")
        title = get_object_or_404(
            Title,
            id=int(self.context.get("view").kwargs.get('title_id'))
        )
        if request and hasattr(request, "user"):
            user = request.user
        if Review.objects.filter(author=user, title=title).exists():
            raise ValidationError("Вы уже оставили отзыв на это произведение.")
        return value
