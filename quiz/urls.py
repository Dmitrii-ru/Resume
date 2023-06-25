from django.urls import path
from . import views


app_name = 'quiz_urls'

urlpatterns = [
    path('', views.index_quiz, name='index_quiz'),
    path('<quiz_pk>/hard', views.quiz_questions, name='quiz_detail_hand'),
    path('<quiz_pk>/easy', views.quiz_questions_paginate, name='quiz_detail_easy'),
    path('<quiz_pk>/quiz_finish', views.quiz_finish, name='quiz_finish'),
    # path('create_quiz', views.create_quiz, name='create_quiz'),
    # path('update_quiz/<quiz_pk>', views.update_quiz, name='update_quiz'),
    path('<quiz_pk>/restart_test', views.restart_test, name='restart_test'),
    # path('create_quiz2', views.create_quiz2, name='create_quiz2'),

]
