from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrModeratorOrReadOnly)
from .serializers import (AdminSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenConfirmationSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class UserCreation(APIView):
    """Вьюсет создания юзера и отправки сообщения на почту"""

    @staticmethod
    def send_participation_code(user_data):
        return send_mail(
            user_data['subject'],
            user_data['message'],
            settings.EMAIL_HOST_USER,
            [user_data['to_email']],
        )

    @staticmethod
    def token_generator(signed_user):
        return default_token_generator.make_token(signed_user)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            signed_user, created = User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            return Response(
                settings.USERNAME_EXISTS_MESSAGE if
                User.objects.filter(username='username').exists()
                else settings.EMAIL_EXISTS_MESSAGE,
                status=HTTPStatus.BAD_REQUEST
            )
        signed_user.confirmation_code = self.token_generator(signed_user)
        user_data = {
            'subject': f'Код подтверждения для {signed_user.username}',
            'message': signed_user.confirmation_code,
            'to_email': signed_user.email
        }

        self.send_participation_code(user_data)
        return Response(serializer.data, status=HTTPStatus.OK)


class JWTTokenConfirmation(APIView):
    """Создание JWT токена через код пользователя"""

    def post(self, request):
        serializer = TokenConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        current_user = get_object_or_404(
            User, username=user_data.get('username'),
        )
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(current_user,
                                               confirmation_code):
            refreshed_token = RefreshToken.for_user(current_user)
            return Response({
                'JWT-Код': str(refreshed_token.access_token),
            }, status=HTTPStatus.CREATED)
        return Response(
            'Неверный код-подтверждение!',
            status=HTTPStatus.BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет Users."""
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('patch', 'post', 'get', 'delete',)
    permission_classes = (IsAdmin, )
    pagination_class = LimitOffsetPagination

    @action(detail=False, url_path='me', methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,))
    def get_or_patch_self_profile(self, request):
        """Пользователь может изменить и получить данные о себе."""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """Вьюсет для жанра."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведения."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ['name', 'year']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.get_title().id
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.get_review().id
        )
