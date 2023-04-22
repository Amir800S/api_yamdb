from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, JWTTokenConfirmation,
                    TitleViewSet, UserCreation, UserViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserCreation.as_view(),
         name='signup'),
    path('v1/auth/token/', JWTTokenConfirmation.as_view(),
         name='token'),
]
