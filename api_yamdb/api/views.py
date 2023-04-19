from http import HTTPStatus

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, User

from .permissions import IsAdmin
from .serializers import (AdminSerializer, CategorySerializer, GenreSerializer,
                          RegistrationSerializer, TitleSerializer,
                          TokenConfirmationSerializer, UserSerializer)


class UserCreation(APIView):
    """Вьюсет создания юзера и отправки сообщения на почту"""
    permission_classes = (AllowAny, )

    @staticmethod
    def send_participation_code(user_data):
        message = EmailMessage(
            subject=user_data['subject'],
            body=user_data['message'],
            from_email=settings.EMAIL_HOST_USER,
            to=[user_data['to_email']],
        )
        message.send()

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            signed_user = serializer.save()
            user_data = {
                'subject': f'Код подтверждения для {signed_user.username}',
                'message': f'{signed_user.confirmation_code}',
                'to_email': signed_user.email
            }
            self.send_participation_code(user_data)
            return Response({
                'username': signed_user.username,
                'email': signed_user.email
            }, status=HTTPStatus.OK, )
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class JWTTokenConfirmation(APIView):
    """Создание JWT токена через код пользователя"""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenConfirmationSerializer(data=request.data)
        serializer.is_valid()
        user_data = serializer.validated_data
        current_user = get_object_or_404(
            User, confirmation_code=user_data['confirmation_code']
        )
        if user_data['confirmation_code'] == current_user.confirmation_code:
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
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = LimitOffsetPagination

    @action(detail=False, url_path='me', methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,))
    def get_or_patch_self_profile(self, request):
        """Пользователь может изменить и получить данные о себе."""
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTPStatus.OK)
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TitleSerializer
