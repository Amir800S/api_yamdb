from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (UserCreation, JWTTokenConfirmation, UserViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns= [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserCreation.as_view(),
         name='signup'),
    path('v1/auth/token/', JWTTokenConfirmation.as_view(),
         name='get_token'),
]