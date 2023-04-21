from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ratings.models import Comment, Review
from reviews.models import User, Title, Genre, Category

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
        if request and hasattr(request, "user"):
            user = request.user
        if Review.objects.filter(author=user).exists():
            raise ValidationError("Вы уже оставили отзыв на это произведение.")
        return value
