from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import RandomPostAPIView,CategoryPostAPIView
from .views import *
app_name = 'mptt_blog_api'

urlpatterns = [
    path('categories', CategoriesAPIView.as_view({'get': 'list'}), name='categories-list'),
    path('categories/<int:id>', CategoriesAPIView.as_view({'get': 'list'}), name='categories-detail'),

    path('categories/create', CategoryCreateViewAPI.as_view(), name='category-create'),
    path('categories/<int:id>/create', CategoryCreateViewAPI.as_view(), name='category-create'),

    path('categories/<int:id>/delete', CategoryUpDelViewAPI.as_view(), name='category-delete'),
    path('categories/<int:id>/update', CategoryUpDelViewAPI.as_view(), name='category-update'),

]
