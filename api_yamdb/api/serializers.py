from statistics import mean

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
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


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер простого юзера: Невозможно поменять роль."""
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(validate_regex_username, ))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'last_name',
            'first_name',
            'role',
            'bio',
        )
        read_only_fields = ('role',)


class TokenConfirmationSerializer(serializers.ModelSerializer):
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
    email = serializers.EmailField(required=True, max_length=254,)
    username = serializers.CharField(required=True, max_length=150,
                                     validators=(
                                         validate_username,
                                         validate_regex_username))

    def validate(self, data):
        """Валидация целиком и отдельно по полям."""
        if not User.objects.filter(
            username=data['username'], email=data['email']
        ):
            if User.objects.filter(username=data['username']):
                raise serializers.ValidationError('Никнейм уже существует!')
            if User.objects.filter(email=data['email']):
                raise serializers.ValidationError('Email уже существует!')
        return data

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
