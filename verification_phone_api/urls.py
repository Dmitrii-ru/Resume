from .views import send_code_verification, invite_code_verification, ProfileUser
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include

app_name = 'verification_phone_api'

urlpatterns = [
    path('send_code', send_code_verification, name='code_verification_api'),
    path('invite_code', invite_code_verification, name='invite_code_verification_api'),
    path('profile/<phone_number>', ProfileUser.as_view(), name='profile')
]

with open('verification_phone_api/swagger/description_text.txt', 'r') as file:
    description_text = file.read()

schema_view_verification_phone = get_schema_view(
    openapi.Info(

        title="Verification Phone API",
        default_version='v1',
        description=description_text,
        contact=openapi.Contact(email="nochev1@mail.ru"),


    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/verification_phone/', include('verification_phone_api.urls'))]
)

urlpatterns += [
    path('docs/', schema_view_verification_phone.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc-verification_phone'
         ),

    path('docs-swagger/', schema_view_verification_phone.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-verification_phone'
         ),
]
