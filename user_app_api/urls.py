from rest_framework.routers import DefaultRouter
from .views import UserRegisterAPIView, LoginAPIView, RefreshTokenView
from django.urls import path

app_name = 'user_app_api'

# router = DefaultRouter()
# router.register('registration', UserRegisterAPIView, basename='user_registration_api')

urlpatterns = [
    path('registration', UserRegisterAPIView.as_view(), name='user_registration_api'),
    path('login', LoginAPIView.as_view(), name='login_api'),
    path('refresh', RefreshTokenView.as_view(), name='refresh_api')
]
# ] + router.urls
