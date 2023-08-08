from rest_framework import serializers
from mptt_blog.models import Post, User, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')


class CategorySerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Category
        fields = ('title', 'id', 'author')


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()
    is_favour = serializers.BooleanField(read_only=True)
    is_like = serializers.BooleanField(read_only=True)
    bread_crumbs = serializers.CharField()
    favourites = serializers.CharField()
    likes = serializers.CharField()

    class Meta:
        model = Post
        fields = '__all__'


class CategoryPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
