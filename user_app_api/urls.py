from .views import UserRegisterAPIView, LoginAPIView, RefreshTokenView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include

app_name = 'user_app_api'

urlpatterns = [
    path('registration', UserRegisterAPIView.as_view(), name='user_registration_api'),
    path('login', LoginAPIView.as_view(), name='login_api'),
    path('refresh', RefreshTokenView.as_view(), name='refresh_api'),
]

schema_use_app_api = get_schema_view(
    openapi.Info(
        title="Verification Phone API",
        default_version='v1',
        description="",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('v1/user_app/', include('user_app_api.urls'))]
)

urlpatterns += [

    path('docs/',
         schema_use_app_api.with_ui(
             'redoc', cache_timeout=0), name='schema-redoc-use_app_api'
         ),
    path('docs-swagger/',
         schema_use_app_api.with_ui(
             'swagger', cache_timeout=0), name='schema-swagger-use_app_api'
         ),
]
