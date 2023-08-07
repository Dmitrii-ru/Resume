from django.urls import path, include

app_name = 'mptt_blog_api'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mptt_blog.models import Post
from .serializers import PostSerializer
from mptt_blog.utils import random_posts
from django.db.models import Q, OuterRef, Exists, Subquery
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import PostSerializer


class RandomPostAPIView(ReadOnlyModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        post_qs = Post.objects.select_related('author').select_related('category').all().order_by('-created')
        return post_qs

    def list(self, request, *args, **kwargs):
        post_qs = self.get_queryset()
        if self.request.user.is_authenticated:
            # Получаем id постов которые публичные или юзер автор
            r_posts = random_posts(
                Post.objects.filter(Q(is_privat=False) | Q(author=self.request.user)).values_list('id', flat=True))

            post_qs = post_qs.filter(pk__in=r_posts).annotate(
                is_favour=Exists(Post.objects.filter(pk=OuterRef('pk'), favourites=self.request.user)),
                is_like=Exists(Post.objects.filter(pk=OuterRef('pk'), likes=self.request.user)),
            )
        else:
            post_qs = random_posts(post_qs.filter(is_privat=False))

        for p in post_qs:

            branch = p.category.get_ancestors(ascending=True, include_self=True)
            p.links = [[p.title, p.url] for p in branch.reverse()]

        data = self.get_serializer(post_qs, many=True).data
        return Response(data)
