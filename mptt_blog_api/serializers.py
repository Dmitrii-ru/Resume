from rest_framework import serializers
from mptt_blog.models import Post, User, Category
from .models import CategoryBlog


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
    favourites = serializers.CharField()
    likes = serializers.CharField()

    class Meta:
        model = Post
        fields = '__all__'


class CategoryPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Validata title

    Every parent has unique children.

    """

    title = serializers.CharField(max_length=50, min_length=3)

    class Meta:
        model = Category
        fields = ('title',)

    def validate_title(self, value):
        title = value
        parent = self.instance.parent if self.instance else self.context.get('parent')

        if parent:
            list_title = list(parent.get_children().values_list('title', flat=True))
        else:
            list_title = list(CategoryBlog.objects.filter(level=0).values_list('title', flat=True))

        if self.instance:
            list_title.remove(self.instance.title)

        list_title = list(map(str.lower, list_title))

        if title.lower() in list_title:
            raise serializers.ValidationError('Not a unique field')
        return value


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBlog
        fields = ('id', 'parent', 'title', 'author')

    def get_fields(self):
        fields = super(CategoriesSerializer, self).get_fields()
        fields['childrens'] = CategoriesSerializer(many=True, required=False)
        return fields
