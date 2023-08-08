from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RandomPostAPIView,CategoryPostAPIView

app_name = 'mptt_blog_api'

urlpatterns = [
    path('', RandomPostAPIView.as_view({'get': 'list'}), name='random_post_api'),
    path('posts_of_category/<path:slug_category>/', CategoryPostAPIView.as_view({'get': 'list'}), name='posts_of_category_api'),
]
