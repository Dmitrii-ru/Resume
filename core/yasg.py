from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include

with open('verification_phone_api/q.txt', 'r') as file:
    description_text = file.read()
app_name = 'verification_phone_api'

# Определение информации о вашем API
schema_view_verification_phone = get_schema_view(
    openapi.Info(
        title="Verification Phone API",
        default_version='v1',
        description=description_text,
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/verification_phone/', include('verification_phone_api.urls'))]
)

urlpatterns = [
    path('api/verification_phone/docs/', schema_view_verification_phone.with_ui('swagger', cache_timeout=0), name='schema-swagger-verification_phone'),
]