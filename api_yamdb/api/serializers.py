from rest_framework import serializers
from reviews.models import Category, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = "slug"
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = "slug"
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


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
