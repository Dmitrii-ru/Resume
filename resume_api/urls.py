from django.urls import path, include
from rest_framework import permissions
from .views import resume_api, feedback_api, ProjectsAPIReadOnly, \
    todo_change_status_api, ProjectDetailAPIReadOnly, TodoViewApi, todo_delete_api
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'resume_api'

urlpatterns = [
    path('', resume_api, name='index'),
    path('feedback', feedback_api, name='feedback'),
    path('projects/<stack_slug>', ProjectsAPIReadOnly.as_view({'get': 'list'}), name='products_list'),
    path('projects/<stack_slug>/<project_slug>/', ProjectDetailAPIReadOnly.as_view({'get': 'list'}),
         name='product_detail'),
    path('todo/<slug_day>', TodoViewApi.as_view(), name='todo_get_post'),
    path('todo/<slug_day>/status', todo_change_status_api, name='todo_status'),
    path('todo/<slug_day>/delete', todo_delete_api, name='todo_delete'),
]
with open('resume_api/swagger/description_text.txt', 'r') as file:

    description_text = file.read()

schema_use_resume_api = get_schema_view(
    openapi.Info(
        title="Resume API",
        default_version='v1',
        description=description_text,
        contact=openapi.Contact(email="nochev1@mail.ru"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/v1/resume/', include('resume_api.urls'))]
)

urlpatterns += [

    path('docs/',
         schema_use_resume_api.with_ui(
             'redoc', cache_timeout=0), name='schema-redoc-resume_api'
         ),
    path('docs-swagger/',
         schema_use_resume_api.with_ui(
             'swagger', cache_timeout=0), name='schema-swagger-resume_api'
         ),
]
