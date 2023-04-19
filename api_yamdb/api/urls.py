from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
UserCreation, JWTTokenConfirmation, UserViewSet,
CategoryViewSet, GenreViewSet, TitleViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns= [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserCreation.as_view(),
         name='signup'),
    path('v1/auth/token/', JWTTokenConfirmation.as_view(),
         name='token'),
]

