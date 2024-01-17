from django.db.models import Prefetch
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import messages
from django.core.paginator import Paginator


def index_quiz(request):
    quizs = Quiz.objects.all()
    context = {
        'quizs': quizs,
    }

    return render(request, 'quiz/index_quiz.html', context)


def update_is_user_answer(user_answer, request, answers):
    for ans in answers.filter(id__in=user_answer):
        ans.is_user_answer.add(request.user)


def del_is_user_answer(answers, request):
    for ans in answers:
        ans.is_user_answer.remove(request.user)

from django.http import HttpResponse
@login_required
def quiz_questions(request, **kwargs):
    quiz = get_object_or_404(Quiz, pk=kwargs['quiz_pk'])
    if request.user in quiz.is_completed.all():
        return redirect('quiz_urls:quiz_finish', kwargs['quiz_pk'])

    questions_qs = Question.objects.filter(parent_quiz=quiz)
    if not questions_qs.exists():
        return HttpResponse(f"<h1>Тест {quiz.title} на стадии разработки ,<a href='{request.META['HTTP_REFERER']}'> "
                            f"вернуться? </a></h1> ")
    question = questions_qs.filter(~Q(is_completed=request.user)).first()

    if not question:
        quiz.is_completed.add(request.user)
        return redirect('quiz_urls:quiz_finish', kwargs['quiz_pk'])

    answers = Answer.objects.filter(parent_question=question)
    number_question = list(questions_qs.values_list('id', flat=True)).index(question.id) + 1
    len_quiz = len(questions_qs)

    if request.method == 'POST':
        if request.POST.getlist('answer'):
            user_answer = list(map(int, (request.POST.getlist('answer'))))
            right_answer = list(answers.filter(is_true=True).values_list('pk', flat=True))

            question.is_completed.add(request.user)
            del_is_user_answer(answers, request)
            update_is_user_answer(user_answer, request, answers)

            if sorted(user_answer) == sorted(right_answer):
                question.is_right_user_completed.add(request.user)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.get_messages(request).used = True
            messages.error(request, f"Нужен хотя бы 1 ответ")

    context = {
        'quiz': quiz,
        'question': question,
        'answers': answers,
        'len_quiz': len_quiz,
        'number_question': number_question,

    }

    return render(request, 'quiz/quiz_detail.html', context)


@login_required
def quiz_finish(request, **kwargs):
    quiz = get_object_or_404(Quiz, pk=kwargs['quiz_pk'])
    questions_qs = Question.objects.filter(parent_quiz=quiz)

    right_user_answer = float(len(questions_qs.filter(is_right_user_completed=request.user)))
    questions_count = float(len(questions_qs))
    percent = int(((right_user_answer - questions_count) / questions_count * 100) + 100)
    percent_negative = 100 - percent
    context = {'percent': percent,
               'percent_negative': percent_negative,
               'right_user_answer': int(right_user_answer),
               'questions_count': int(questions_count),
               'quiz': quiz,
               }
    return render(request, 'quiz/finish_quiz.html', context=context)


@login_required
def quiz_questions_paginate(request, **kwargs):
    quiz = get_object_or_404(Quiz.objects, pk=kwargs['quiz_pk'])
    if request.user in quiz.is_completed.all():
        return redirect('quiz_urls:quiz_finish', kwargs['quiz_pk'])

    # Каждому вопросу добавляем users_completed_list со списком юзеров которые ответили на это вопрос
    questions_qs = Question.objects.filter(parent_quiz=quiz).prefetch_related(
        Prefetch('is_completed', to_attr='users_completed_list'))
    if not questions_qs.exists():
        return HttpResponse(f"<h1>Тест {quiz.title} на стадии разработки ,<a href='{request.META['HTTP_REFERER']}'> "
                            f"вернуться? </a></h1> ")
    finish_flag = True
    pag_qs = []
    len_quiz = len(questions_qs)

    for q in questions_qs:
        # если это вопрос уже решался то, добавляем
        if request.user in q.users_completed_list:
            pag_qs.append(q)
        else:
            finish_flag = False
            # если не решался то, добавим что бы всегда был 1 не решенный вопрос
            pag_qs.append(q)
            break
    if finish_flag:
        quiz.is_completed.add(request.user)
        return redirect('quiz_urls:quiz_finish', kwargs['quiz_pk'])

    paginator = Paginator(pag_qs, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    question = page_obj.object_list[0]

    answers = Answer.objects.filter(parent_question=question)
    answers_ids = {x.id: i for i, x in enumerate(answers)}
    for answers_id in request.user.user_answer.filter(id__in=list(answers_ids.keys())).values_list('id', flat=True):
        answers[answers_ids[answers_id]].user_answer = True

    if request.method == 'POST':
        if request.POST.getlist('answer'):
            user_answer = list(map(int, (request.POST.getlist('answer'))))
            right_answer = list(answers.filter(is_true=True).values_list('pk', flat=True))

            del_is_user_answer(answers, request)
            question.is_completed.add(request.user)
            update_is_user_answer(user_answer, request, answers)

            if sorted(user_answer) == sorted(right_answer):
                question.is_right_user_completed.add(request.user)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.get_messages(request).used = True
            messages.error(request, f"Нужен хотя бы 1 ответ")

    context = {
        'quiz': quiz,
        'question': questions_qs,
        'page_obj': page_obj,
        'answers': answers,
        'len_quiz': len_quiz,

    }
    return render(request, 'quiz/quiz_detail_pag.html', context)


def restart_test(request, **kwargs):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions'), id=kwargs['quiz_pk'])
    answer = Answer.objects.filter(parent_question__parent_quiz=quiz).select_related('parent_question__parent_quiz')
    request.user.user_answer.remove(*list(answer))
    request.user.completed.remove(*list(quiz.questions.all()))
    request.user.right_completed.remove(*list(quiz.questions.all()))
    quiz.is_completed.remove(request.user)
    return redirect('quiz_urls:index_quiz')
