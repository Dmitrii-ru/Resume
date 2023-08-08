from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404 as api404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from mptt_blog.models import Post, Category
from mptt_blog.utils import random_posts
from django.db.models import Q, OuterRef, Exists
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import PostSerializer, CategoryPostsSerializer, CategorySerializer


class RandomPostAPIView(ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        post_qs = Post.objects.select_related('author').select_related('category__author').all().order_by('-created')
        return post_qs

    @swagger_auto_schema(
        operation_description="Список случайных постов",
        responses={200: PostSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        print(request.user)
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
            p.bread_crumbs = [[p.title, p.url] for p in branch.reverse()]

        data = self.get_serializer(post_qs, many=True).data
        return Response(data)


class PaginatorCategoryPost(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 8


def update_page_data_like_fav(request, page):
    if request.user.is_authenticated:
        post_ids = {x.id: i for i, x in enumerate(page)}

        for post_id in request.user.favourite_posts.filter(
                id__in=list(post_ids.keys())).values_list('id', flat=True):
            page[post_ids[post_id]].is_favour = True

        for post_id in request.user.like_posts.filter(
                id__in=list(post_ids.keys())).values_list('id', flat=True):
            page[post_ids[post_id]].is_like = True

    return page


class CategoryPostAPIView(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = CategoryPostsSerializer
    pagination_class = PaginatorCategoryPost

    def get_queryset(self):
        post_qs = Post.objects.select_related('author').select_related('category__author').filter(
            Q(category__url=self.kwargs['slug_category'])
        )

        if self.request.user.is_authenticated:
            post_qs = post_qs.filter(
                Q(is_privat=False) | Q(author=self.request.user))

        else:
            post_qs = post_qs.filter(is_privat=False)
        qs = {

            'post_qs': post_qs,
        }
        return qs

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        extra_data = {}
        c = api404(Category.objects.select_related('author'), url=self.kwargs['slug_category'])
        extra_data['category'] = CategorySerializer(c).data
        extra_data['category_children'] = CategorySerializer(c.get_children(), many=True).data
        extra_data['category_parents'] = CategorySerializer(
            c.get_ancestors(ascending=False, include_self=False),
            many=True).data
        response.data.update({'extra_data': extra_data})
        return response

    def list(self, request, *args, **kwargs):
        data = {}
        qs = self.get_queryset()['post_qs']
        queryset = self.filter_queryset(qs)
        page = self.paginate_queryset(queryset)
        if page is not None:
            page = update_page_data_like_fav(self.request, page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True).data
        data['serializer'] = serializer

        return Response(data)
