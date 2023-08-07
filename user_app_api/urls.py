from rest_framework.routers import DefaultRouter
from .views import UserRegisterAPIView
from django.urls import path
app_name = 'user_app_api'

# router = DefaultRouter()
# router.register('registration', UserRegisterAPIView, basename='user_registration_api')

urlpatterns = [
    path('registration', UserRegisterAPIView.as_view(), name='user_registration_api')
]
# ] + router.urls
