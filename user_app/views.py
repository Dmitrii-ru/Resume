import os

from django.shortcuts import render, get_object_or_404

from core import settings
from .forms import UserRegisterForm, UserUpdateForm, ProfileImageForm, CustomPasswordResetForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

from django.contrib.auth.views import PasswordResetView
from .models import Profile
from .user_session import UserSessionApp, UserSessionToDo, UserSessionEmail
from mptt_blog.models import Category, Post, CommentsPost
from quiz.models import Quiz, Question
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from resume.models import EmailSettings


def create_previous_path(req_meta_path, req_path, usa):
    if req_path not in req_meta_path:
        usa.profile_previous_path(req_meta_path)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            redirect_to = request.GET.get('next')

            if redirect_to:
                return HttpResponseRedirect(reverse_lazy('user_urls:user') + '?next=' + redirect_to)
            else:
                return redirect('user_urls:user')

    else:
        form = UserRegisterForm
    return render(request, 'user_app/registration.html', {'form': form})


@login_required
def profile(request):
    usa = UserSessionApp(request)
    create_previous_path(request.META.get('HTTP_REFERER', '/'), request.path, usa)

    if request.method == "POST":
        UpdateImageForm = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        UpdateUserForm = UserUpdateForm(request.POST, instance=request.user)

        user_profile = get_object_or_404(Profile, user=request.user)
        # Берем старое имя
        old_name = os.path.basename(user_profile.img.path)
        # Спрашиваем явиться ли оно default для img
        bool_default_img = old_name == user_profile._meta.get_field('img').default

        if UpdateImageForm.is_valid() and UpdateUserForm.is_valid():

            UpdateImageForm.save()
            UpdateUserForm.save()

            if request.FILES.get('img') and os.path.exists(user_profile.img.path) and not bool_default_img:
                os.remove(user_profile.img.path)
            return redirect('user_urls:profile')

    else:
        UpdateImageForm = ProfileImageForm(instance=request.user.profile)
        UpdateUserForm = UserUpdateForm(instance=request.user)
    data = {
        'UpdateImageForm': UpdateImageForm,
        'UpdateUserForm': UpdateUserForm,
        'title': "Ваш профиль",
        'previous_path': usa.get_profile_previous_path(),

    }

    return render(request, 'user_app/profile.html', data)


from django.db.models import Count, Prefetch


def quiz_completed_statistics(user):
    count_quiz = 0
    percent = 0
    quizs = Quiz.objects.filter(is_completed=user).prefetch_related(
        Prefetch('questions', to_attr='questions_qa'),
        Prefetch('questions', queryset=Question.objects.filter(is_right_user_completed=user),
                 to_attr='is_right_user_completed')
    )

    if quizs:
        questions_count = 0
        questions_count_right = 0
        for q in quizs:
            questions_count += len(q.questions_qa)
            questions_count_right += len(q.is_right_user_completed)
        percent = int(((questions_count_right - questions_count) / questions_count * 100) + 100)
        count_quiz = len(quizs)

    return {'count_quiz': count_quiz, 'percent_positive': percent}


def person_area_view(request):
    data = {}
    ust = UserSessionToDo(request)
    todo_actual_session = ust.get_actual_todo()
    use = UserSessionEmail(request)
    data['count_mail'] = use.user_session_email['email_count']
    data['count_cat'] = 0
    data['count_post'] = 0
    data['count_comm'] = 0
    data['count_quiz'] = 0
    data['quiz_percent_positive'] = 0
    if request.user.is_authenticated:
        count_cat = Category.objects.filter(author=request.user).aggregate(count_cat=Count('id'))
        count_post = Post.objects.filter(author=request.user).aggregate(count_post=Count('id'))
        count_comm = CommentsPost.objects.filter(author=request.user).aggregate(count_comm=Count('id'))
        quiz_statistics = (quiz_completed_statistics(request.user))
        data['quiz_percent_positive'] = quiz_statistics['percent_positive']
        data['count_quiz'] = quiz_statistics['count_quiz']
        data['count_cat'] = count_cat['count_cat']
        data['count_post'] = count_post['count_post']
        data['count_comm'] = count_comm['count_comm']
    data['todo_actual_session'] = todo_actual_session['list_actual']
    data['count_todo'] = todo_actual_session['count_actual']
    return render(request, 'user_app/person_area.html', data)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        user_session_todo = request.session.get('user_session_todo')
        user_session = request.session.get('user_session')
        user_session_email = request.session.get('user_session_email')
        response = super().dispatch(request, *args, **kwargs)
        if user_session_todo:
            request.session['user_session_todo'] = user_session_todo
        elif user_session:
            request.session['user_session'] = user_session
        elif user_session_email:
            request.session['user_session_email'] = user_session_email
        request.session.save()
        return response


class CustomPasswordResetView(PasswordResetView):
    template_name = 'user_app/pass-reset.html'
    email_template_name = "user_app/password_reset_form.html"

    form_class = CustomPasswordResetForm

    # def form_valid(self, form):
    #     try:
    #
    #         return super().form_valid(form)
    #
    #     except:
    #         return HttpResponse("Ошибка отправки электронной почты для восстановления пароля")

