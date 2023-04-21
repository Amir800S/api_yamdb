from rest_framework import serializers
from reviews.models import Category, Genre, Title, User

from .validators import validate_username, validate_regex_username


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
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
            'bio',
            'role'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер простого юзера: Невозможно поменять роль."""
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[validate_regex_username])

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
                                     validators=(validate_username,
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
