from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from mptt.querysets import TreeQuerySet
from mptt.templatetags.mptt_tags import cache_tree_children

from .models import Category, Post, CommentsPost
from .forms import CategoryCreateForm, PostCreateForm, CategoryUpdateForm, PostUpdateForm, CommentsPostForm
from django.urls import reverse
from django.db.models import Q, OuterRef, Exists, Subquery
from rules.contrib.views import PermissionRequiredMixin

from .utils import random_posts

like_text = 'Понравилась'
UnLike_text = 'Поставить Like'
fav_false_text = 'Нет в избранных'
fav_true_text = 'В избранных'


class RandomPostView(ListView):
    model = Category
    template_name = "mptt_blog/category/category_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_qs = Post.objects.select_related('author').select_related('category').all().order_by('-created')
        if self.request.user.is_authenticated:
            # Получаем id постов которые публичные или юзер автор
            r_posts = random_posts(
                Post.objects.filter(
                    Q(is_privat=False) | Q(author=self.request.user)
                ).values_list('id', flat=True)
            )

            post_qs = post_qs.filter(pk__in=r_posts).annotate(
                is_favour=Exists(Post.objects.filter(pk=OuterRef('pk'), favourites=self.request.user)),
                is_like=Exists(Post.objects.filter(pk=OuterRef('pk'), likes=self.request.user)),
            )

        else:
            post_qs = random_posts(post_qs.filter(is_privat=False))

        for p in post_qs:
            branch = p.category.get_ancestors(
                ascending=True,
                include_self=True
            )
            p.links = [[p.title, p.url] for p in branch.reverse()]

        context['posts'] = post_qs
        context['like_text'] = like_text
        context['UnLike_text'] = UnLike_text
        context['fav_false_text'] = fav_false_text
        context['fav_true_text'] = fav_true_text

        return context


class CategoryMPTTView(ListView):
    model = Category
    template_name = "mptt_blog/category/category_mptt.html"
    queryset = None
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category.objects.select_related('author'), url=self.kwargs['slug_cat'])
        cats = category.get_children()
        parents = category.get_ancestors(ascending=False, include_self=True)
        context['cats'] = cats
        context['parents'] = parents
        context['category'] = category
        context['root'] = category.get_root()
        context['like_text'] = like_text
        context['UnLike_text'] = UnLike_text
        context['fav_false_text'] = fav_false_text
        context['fav_true_text'] = fav_true_text
        if self.request.user.is_authenticated:

            post_ids = {x.id: i for i, x in enumerate(context['page_obj'].object_list)}

            for post_id in self.request.user.favourite_posts.filter(
                    id__in=list(post_ids.keys())).values_list('id', flat=True):
                context['page_obj'].object_list[post_ids[post_id]].is_favour = True

            for post_id in self.request.user.like_posts.filter(
                    id__in=list(post_ids.keys())).values_list('id',flat=True):
                context['page_obj'].object_list[post_ids[post_id]].is_like = True

        return context

    def get_queryset(self):
        category = get_object_or_404(Category, url=self.kwargs['slug_cat'])
        post_qs = Post.objects.select_related('author').filter(Q(category=category))

        if self.request.user.is_authenticated:
            post_qs = post_qs.filter(
                Q(is_privat=False) | Q(author=self.request.user)
            )

        else:
            post_qs = post_qs.filter(is_privat=False)
        return post_qs


class CategoryCreateView(PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'mptt_blog/category/create_topic.html'
    form_class = CategoryCreateForm
    permission_required = ('is_user_authenticated',)

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        category = None
        if self.kwargs:
            category = get_object_or_404(Category, url=self.kwargs['slug_cat'])
            context['title'] = 'Создать тему в '
        else:
            context['title'] = 'Создать категорию'
        context['btn'] = 'Добавить'
        context['obj'] = category
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'mptt_blog/category/update_topic.html'
    form_class = CategoryUpdateForm
    permission_required = ('is_author',)

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['btn'] = 'Обновить'
        context['title'] = 'Обновить тему'
        return context


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'mptt_blog/delete.html'
    permission_required = ('is_author',)

    def get_success_url(self):
        if self.object.parent:
            return reverse('mptt_blog_urls:category_mptt', kwargs={'slug_cat': self.object.parent.url})
        return reverse('mptt_blog_urls:category-list')


class PostDetailView(PermissionRequiredMixin, DetailView, FormMixin):
    form_class = CommentsPostForm
    model = Post
    template_name = 'mptt_blog/post/post_detail.html'
    permission_required = ('is_odj_private',)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['comments'] = self.object.comments.select_related('author').all().annotate(
                is_likes=Exists(CommentsPost.objects.filter(pk=OuterRef('pk'), likes=self.request.user)))

        context['favourite_flag'] = self.object.favourites.filter(id=self.request.user.id).exists()
        context['like_flag'] = self.object.likes.filter(id=self.request.user.id).exists()
        context['like_text'] = like_text
        context['UnLike_text'] = UnLike_text

        return context

    def get_object(self):
        post = Post.objects.select_related('author').get(pk=self.kwargs['pk'])
        return post

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if request.user.is_authenticated:
            if form.is_valid():
                CommentsPost(
                    text=form.cleaned_data.get('text'),
                    author=self.request.user,
                    post=self.get_object()
                ).save()

                return redirect(request.META.get('HTTP_REFERER'))
            return self.form_invalid(form)
        return redirect('user_urls:reg')

    # return render(self.request, 'mptt_blog/post/post_detail.html', context=self.get_context_data())


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'mptt_blog/post/post_create_update.html'
    form_class = PostCreateForm
    permission_required = ('is_user_authenticated',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, url=self.kwargs['slug_cat_create_post'])
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['btn'] = 'Добавить'
        context['title'] = 'Создать сталью'
        context['category'] = category
        return context


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'mptt_blog/post/post_create_update.html'
    form_class = PostUpdateForm
    permission_required = ('is_author',)

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['btn'] = 'Обновить'
        context['title'] = 'Обновить'
        return context


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'mptt_blog/delete.html'
    permission_required = ('is_author',)

    def get_success_url(self):
        return reverse('mptt_blog_urls:category_mptt', kwargs={'slug_cat': self.object.category.url})


def comment_post_delete(request, *args, **kwargs):
    obj = get_object_or_404(CommentsPost.objects.select_related('author'), pk=kwargs['pk'])
    if request.user == obj.author:
        obj.delete()
    return HttpResponseRedirect(
        reverse('mptt_blog_urls:post_detail', kwargs={'slug_cat': kwargs['slug_cat'], 'pk': kwargs['pk_post']}))


@login_required
def favourites_add_rem(request, *args, **kwargs):
    post = get_object_or_404(Post, pk=kwargs['pk_post_fav'])
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(
        reverse('mptt_blog_urls:post_detail', kwargs={'slug_cat': kwargs['slug_cat'], 'pk': kwargs['pk_post_fav']}))


class PostFavouritesShowAll(PermissionRequiredMixin, ListView):
    model = Post
    queryset = None
    paginate_by = 7
    context_object_name = 'posts'
    template_name = 'mptt_blog/post/favourites.html'
    permission_required = ('is_user_authenticated',)

    def get_queryset(self):
        post_qs = Post.objects.select_related('author').select_related('category').filter(
            Q(favourites=self.request.user))
        post_qs = post_qs.filter(Q(is_privat=False) | Q(author=self.request.user)).annotate(
            is_like=Exists(Post.objects.filter(pk=OuterRef('pk'), likes=self.request.user))
        )
        return post_qs

    def get_context_data(self, **kwargs):
        context = super(PostFavouritesShowAll, self).get_context_data(**kwargs)
        context['like_text'] = like_text
        context['UnLike_text'] = UnLike_text
        context['fav_false_text'] = fav_false_text
        context['fav_true_text'] = fav_true_text
        context['category_list'] = Category.objects.filter(level=0)
        return context


@login_required
def like(request):
    if request.POST.get('action') == 'post':
        like_l = UnLike_text
        result = ''
        id_odj = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id_odj)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            like_l = like_text
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        return JsonResponse({'result': result, 'like': like_l})


@login_required
def favourites(request):
    if request.POST.get('action') == 'post':
        fav_btn_text = fav_false_text
        id_odj = int(request.POST.get('postid'))
        post = get_object_or_404(Post.objects, id=id_odj)

        if post.favourites.filter(id=request.user.id).exists():
            post.favourites.remove(request.user)
            post.save()
        else:
            fav_btn_text = fav_true_text
            post.favourites.add(request.user)
            post.save()
        return JsonResponse({'fav_btn_text': fav_btn_text})


@login_required
def like_comment(request):
    if request.POST.get('action') == 'post':
        like_l = UnLike_text
        result = ''
        id_odj = int(request.POST.get('commentid'))
        comment = get_object_or_404(CommentsPost, id=id_odj)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            comment.like_count -= 1
            result = comment.like_count
            comment.save()
        else:
            like_l = like_text
            comment.likes.add(request.user)
            comment.like_count += 1
            result = comment.like_count
            comment.save()
        return JsonResponse({'result': result, 'like': like_l})
