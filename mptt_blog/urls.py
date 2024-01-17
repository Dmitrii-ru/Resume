from django.urls import path, include
from . import views
from .views import RandomPostView, CategoryMPTTView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, \
    PostDetailView, PostUpdateView, PostDeleteView, PostCreateView, PostFavouritesShowAll 

app_name = 'mptt_blog_urls'

urlpatterns = [
    path('', RandomPostView.as_view(), name='category-list'),
    path('like', views.like, name='like'),
    path('fav', views.favourites, name='favourites'),
    path('like-comment', views.like_comment, name='like-comment'),
    path('favourites', PostFavouritesShowAll.as_view(), name='fav_show_all'),
    path('<path:slug_cat>/', CategoryMPTTView.as_view(), name='category_mptt'),
    path('create', CategoryCreateView.as_view(), name='category_no_parent_create'),
    path('<path:slug_cat>/create', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/update', CategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/del', CategoryDeleteView.as_view(), name='category_delete'),
    path('<path:slug_cat>/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('<path:slug_cat_create_post>/create_post', PostCreateView.as_view(), name='post_create'),
    path('<path:slug_cat>/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('<path:slug_cat>/<int:pk>/del', PostDeleteView.as_view(), name='post_del'),
    path('<path:slug_cat>/<int:pk_post>/<int:pk>/del_comm', views.comment_post_delete, name='comm_del'),
    path('<path:slug_cat>/<int:pk_post_fav>/fav', views.favourites_add_rem, name='fav'),

]
