from .views import send_code_verification, invite_code_verification, ProfileUser
from django.urls import path

app_name = 'verification_phone_api'

urlpatterns = [
    path('send_code', send_code_verification, name='code_verification_api'),
    path('invite_code', invite_code_verification, name='invite_code_verification_api'),
    path('profile/<phone_number>', ProfileUser.as_view(), name='profile')
]

