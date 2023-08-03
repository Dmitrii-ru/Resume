from django.urls import path
from .views import resume_api, feedback_api, send_email_api, ProjectsAPIReadOnly, TodoSessionViewAPI, \
    TodoDelReplaceSessionViewAPI
from rest_framework.routers import DefaultRouter

app_name = 'resume_api'

router: DefaultRouter = DefaultRouter()

# router.register('index', resume_api, basename='api_resume_index')

urlpatterns = [
    path('', resume_api, name='api_resume_index'),
    path('feedback', feedback_api, name='api_resume_feedback'),
    path('send_email', send_email_api, name='api_send_email'),
    path('products/<stack_slug>', ProjectsAPIReadOnly.as_view({'get': 'list'}), name='api_products_list'),
    # path('todo_session', TodoSessionViewAPI, name='api_todo_session'),
    path('todo_session/<slug_day>', TodoSessionViewAPI, name='api_todo_session_day'),
    path('todo_session/todo/del_patch', TodoDelReplaceSessionViewAPI, name='todo_session_del'),
]
