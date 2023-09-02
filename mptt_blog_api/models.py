from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from pytils.translit import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

YES = 'True'
NO = 'False'
PRIVATE_CHOICES = (
    (YES, "Все видят"),
    (NO, "Только я"),
)


def category_author_default_post(*args, **kwargs):
    User = get_user_model()
    return User.objects.filter(is_superuser=True).order_by('id').first()


class PostBlog(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=100,
        blank=False
    )
    category = TreeForeignKey(
        'CategoryBlog', on_delete=models.CASCADE,
        related_name='category_post',
        verbose_name='Категория',
        blank=False
    )
    text = RichTextField(
        verbose_name='Текст',
        blank=False
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        default=category_author_default_post
    )
    is_private = models.BooleanField(
        verbose_name='Вижу только я',
        default=False

    )
    favourites = models.ManyToManyField(
        User,
        verbose_name='В избранных',
        related_name='favourites_post',
        default=None,
        blank=True
    )
    likes = models.ManyToManyField(
        User,
        verbose_name='Поставили лайк',
        related_name='likes_post',
        default=None,
        blank=True
    )
    like_count = models.BigIntegerField(
        verbose_name='Количество лайков',
        default='0'
    )
    created = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name='Обновлено',
        auto_now=True
    )

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


def update_branch_urls(obj, old_url):
    update_list = []
    for children in obj.get_descendants(include_self=False):
        update_list.append(
            CategoryBlog(
                id=children.id,
                url=build_url(children.url, old_url, obj.url)
            )
        )
    CategoryBlog.objects.bulk_update(
        update_list,
        fields=['url']
    )


def build_url(children_url, old_url, obj_url):
    return children_url.replace(old_url, obj_url, 1)


class CategoryBlog(MPTTModel):
    title = models.CharField(
        verbose_name='Название',
        max_length=50,

    )
    parent = TreeForeignKey(
        'self',
        verbose_name='Родительская категория',
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name='childrens',
        db_index=True,

    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        null=True,
        default=category_author_default
    )
    url = models.TextField(
        verbose_name='Url адрес'

    )

    def save(self, *args, **kwargs):
        update_branch = False
        old_url = None
        if not self.url:
            self.url = self.build_url()
        elif slugify(self.title) != self.url.split('/')[-1]:
            update_branch = True
            old_url = self.url
            self.url = self.build_url()
        super().save(*args, **kwargs)
        if update_branch:
            update_branch_urls(self, old_url)

    def build_url(self):
        title = slugify(self.title)
        if self.parent:
            url = self.parent.url + '/' + title
        else:
            url = title
        return url

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('mptt_blog_urls:category_mptt', kwargs={'slug_cat': self.url})

    def __str__(self):
        return f'{self.title}'


class CommentsPostBlog(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        null=True,
        default=category_author_default
    )
    post = models.ForeignKey(
        PostBlog,
        on_delete=models.CASCADE,
        verbose_name='Статья',
        related_name='post_comments',
        blank=False
    )
    text = RichTextField(
        verbose_name='Текст',
        max_length=400
    )
    likes = models.ManyToManyField(
        User,
        verbose_name='Поставили лайк',
        related_name='likes_comment',
        default=None,
        blank=True
    )
    like_count = models.BigIntegerField(
        verbose_name='Количество лайков',
        default='0'
    )
    created = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True
    )
