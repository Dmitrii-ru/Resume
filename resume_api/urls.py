from django.urls import path, include
from rest_framework import permissions
from .views import resume_api, feedback_api, send_email_api, ProjectsAPIReadOnly, TodoSessionViewAPI, \
    TodoDeleteSessionViewAPI, TodoPatchSessionViewAPI, ProjectDetailAPIReadOnly
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'resume_api'



urlpatterns = [
    path('', resume_api, name='api_resume_index'),
    path('feedback', feedback_api, name='api_resume_feedback'),
    path('send_email', send_email_api, name='api_send_email'),
    path('products/<stack_slug>', ProjectsAPIReadOnly.as_view({'get': 'list'}), name='api_products_list'),
    path('projects/<stack_slug>/<project_slug>/', ProjectDetailAPIReadOnly.as_view({'get': 'list'}), name='api_product_detail'),
    # path('todo_session', TodoSessionViewAPI, name='api_todo_session'),
    path('todo_session/<slug_day>', TodoSessionViewAPI, name='api_todo_session_day'),
    path('todo_session/<slug_day>/delete', TodoDeleteSessionViewAPI, name='todo_session_delete'),
    path('todo_session/<slug_day>/patch', TodoPatchSessionViewAPI, name='todo_session_patch'),
]



schema_use_app_api = get_schema_view(
    openapi.Info(
        title="Resume API",
        default_version='v1',
        description="",
        contact=openapi.Contact(email="nochev1@mail.ru"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('v1/resume_api/', include('resume_api.urls'))]
)

urlpatterns += [

    path('docs/',
         schema_use_app_api.with_ui(
             'redoc', cache_timeout=0), name='schema-redoc-resume_api'
         ),
    path('docs-swagger/',
         schema_use_app_api.with_ui(
             'swagger', cache_timeout=0), name='schema-swagger-resume_api'
         ),
]
