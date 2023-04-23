from statistics import mean

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=True
    )
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
            return 0


class AdminSerializer(serializers.ModelSerializer):
    """Сериалайзер для админа: Все поля редактируемы."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'confirmation_code',
            'bio',
            'role'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер простого юзера: Невозможно поменять роль."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'last_name',
            'first_name',
            'confirmation_code',
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


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователя."""
    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )


class CommentSerializer(serializers.ModelSerializer):
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
