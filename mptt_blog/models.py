from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from pytils.translit import slugify
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

YES = 'True'
NO = 'False'
PRIVAT_CHOICES = (
    (YES, "Все видят"),
    (NO, "Только я"),
)

def category_author_default_post(*args, **kwargs):

    User = get_user_model()
    return User.objects.filter(is_superuser=True).order_by('id').first()


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    category = TreeForeignKey('Category', on_delete=models.CASCADE, related_name='posts', verbose_name='Категория',
                              blank=True)
    content = RichTextField()
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, blank=False, null=False, default=1)
    is_privat = models.BooleanField('Вижу только я', default=False)
    favourites = models.ManyToManyField(User, related_name='favourite_posts', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='like_posts', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    # Удалить !!!is_fav
    is_fav = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):

        return reverse('mptt_blog_urls:post_detail', kwargs={'slug_cat': self.category.url, 'pk': self.pk})




def category_author_default(*args, **kwargs):
    User = get_user_model()
    return User.objects.filter(is_superuser=True).order_by('id').first()


class Category(MPTTModel):
    title = models.CharField(max_length=50, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, null=True,
                               default=category_author_default)
    url = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.url:
            c = Category.objects.get(pk=self.pk)
            if c.title != self.title:
                self.build_url()
                for children in self.get_descendants(include_self=False):
                    children.build_url()

        if not self.url:
            self.build_url()

    def build_url(self):
        title = slugify(self.title)
        if self.parent:
            self.url = self.parent.url + '/' + title
        else:
            self.url = title
        self.save()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('mptt_blog_urls:category_mptt', kwargs={'slug_cat': self.url})

    def __str__(self):
        return f'{self.title}'


class CommentsPost(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, null=True,
                               default=category_author_default)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='like_comment', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
