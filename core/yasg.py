from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include

with open('verification_phone_api/q.txt', 'r') as file:
    description_text = file.read()

# Определение информации о вашем API
schema_view_verification_phone = get_schema_view(
    openapi.Info(
        title="Verification Phone API",
        default_version='v1',
        description=description_text,
        terms_of_service="description_text",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/verification_phone/', include('verification_phone_api.urls'))]
)

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
    patterns=[path('api/user_app/', include('user_app_api.urls'))]
)
#
#
# schema_mptt_blog_api = get_schema_view(
#     openapi.Info(
#         title="Verification Phone API",
#         default_version='v1',
#         description="",
#         terms_of_service="",
#         contact=openapi.Contact(email=""),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
#     patterns=[path('api/mptt_blog/', include('mptt_blog_api.urls'))]
# )
#
# schema_resume_api = get_schema_view(
#     openapi.Info(
#         title="Verification Phone API",
#         default_version='v1',
#         description="",
#         terms_of_service="",
#         contact=openapi.Contact(email=""),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
#     patterns=[path('api/resume/', include('resume_api.urls'))]
# )
#


urlpatterns = [
    path('api/verification_phone/docs/', schema_view_verification_phone.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc-verification_phone'),

    path('api/verification_phone/docs-swagger/', schema_view_verification_phone.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-verification_phone'),

    path('api/user_app/docs/', schema_use_app_api.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc-use_app_api'),

    path('api/user_app/docs-swagger/', schema_use_app_api.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-use_app_api'),

]
