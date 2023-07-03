from django.urls import path
from . import views
from .views import *

app_name = 'resume_urls'

urlpatterns = [
    path('', views.index, name='index'),
    path('send_email/', views.send_email_view, name='send_email'),
    path('todo_session/', views.TodoSessionView, name='todo_session'),
    path('todo_session/<slug_day>/', views.TodoSessionView, name='todo_session_day'),
    path('todo_session/<slug_day>/del/', views.TodoDelReplaceSessionView, name='todo_session_del'),
    path('todo_session/<slug_day>/remove/', views.TodoDelReplaceSessionView, name='todo_session_remove'),
    path('projects/<stack_slug>/', ProjectsView.as_view(), name='stack'),
    path('projects/<stack_slug>/<project_slug>/', ProjectsDetailView.as_view(), name='proj_detail'),
]
