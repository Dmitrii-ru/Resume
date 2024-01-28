from django.urls import path
from .views import *
app_name = 'mptt_blog_api'

urlpatterns = [
    path('categories', CategoriesAPIView.as_view({'get': 'list'}), name='categories-list'),
    path('category/<int:id>', CategoriesAPIView.as_view({'get': 'list'}), name='category-detail'),

    path('category/create', CategoryCreateViewAPI.as_view(), name='category-create'),
    path('category/<int:id>/create', CategoryCreateViewAPI.as_view(), name='category-create'),

    path('categories/<int:id>/delete', CategoryUpDelViewAPI.as_view(), name='category-delete'),
    path('categories/<int:id>/update', CategoryUpDelViewAPI.as_view(), name='category-update'),
]
