from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RandomPostAPIView

app_name = 'mptt_blog_api'

urlpatterns = [
    path('', RandomPostAPIView.as_view({'get': 'list'}), name='random_post_api'),

]
