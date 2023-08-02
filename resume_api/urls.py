from django.urls import path, include
from .views import resume_api, feedback_api, send_email_api
from rest_framework.routers import DefaultRouter

app_name = 'resume_api'

router: DefaultRouter = DefaultRouter()

# router.register('index', resume_api, basename='api_resume_index')

urlpatterns = [
    path('', resume_api, name='api_resume_index'),
    path('feedback', feedback_api, name='api_resume_feedback'),
    path('send_email', send_email_api, name='api_send_email')

]
