from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
import json
from resume.forms import AddTodo
from resume.python_prog.calendar_session_todo import MyCalendar
from resume.tasks import send_email_task
from resume.cache import count_send_email, get_model_all, get_single_model_obj, get_filter_model, get_model_all_order
from resume.models import AboutMe, MyEducation, Stack, Project
from resume.views import get_ip
from user_app.user_session import UserSessionEmail, UserSessionToDo, get_today, get_date, navigate_month
from .serializers import AboutMeSerializer, MyEducationSerializer, StackSerializer, FeedbackSerializer, \
    EmailSendSerializer, ProductSerializer, AddTodoSerializer


@api_view(['GET'])
def resume_api(request):
    context = {}
    about_me = get_model_all(AboutMe)
    if about_me:
        context['about_me'] = AboutMeSerializer(about_me[0]).data
    context['my_education'] = MyEducationSerializer(get_model_all_order(MyEducation, '-percent'), many=True).data
    context['stacks'] = StackSerializer(get_model_all(Stack), many=True).data
    return Response(context, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=FeedbackSerializer)
@api_view(['POST'])
def feedback_api(request):
    """
    Create a new feedback.

    Create a new feedback object by providing the text in the request body.

    ---
    request_serializer: FeedbackSerializer
    response_serializer: FeedbackSerializer
    """
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=EmailSendSerializer)
@api_view(['POST', 'GET'])
def send_email_api(request):
    ip = get_ip(request)
    stacks = Stack.objects.all()
    user_s = UserSessionEmail(request)
    user_s.update_date_count()
    count = count_send_email(ip)
    count_bool = count < 2

    if count_bool:
        letter = 'письмо' if count == 1 else 'письма'

        if request.method == 'POST':
            serializer = EmailSendSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                name = serializer.validated_data.get('name')
                send_email_task.delay(name=name, to_send=email, subject=1, massage_num=1)
                user_s.update(ip)
                return Response({'success': True,
                                 'message': 'Email sent successfully.'},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'stacks': StackSerializer(stacks, many=True).data,
             'count': abs(count - 2),
             'count_bool': count_bool,
             'letter': letter})
    else:
        return Response(
            {'stacks': StackSerializer(stacks, many=True).data,
             'success': False,
             'message': 'Email limit exceeded.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS)


class ProjectsAPIReadOnly(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        data = {'projects': ProductSerializer(get_filter_model(Project, 'stacks__slug', self.kwargs['stack_slug']),
                                              many=True).data,
                'stacks': StackSerializer(get_model_all(Stack), many=True).data,
                'stack': StackSerializer(get_single_model_obj(Stack, 'slug', self.kwargs['stack_slug'])).data}
        return Response(data)

@swagger_auto_schema(method='post', request_body=AddTodoSerializer)
@api_view(['POST', 'GET'])
def TodoSessionViewAPI(request, **kwargs):
    ust = UserSessionToDo(request)
    form_add_todo = AddTodoSerializer()

    if request.method == "POST":
        request_data = request.data
        post = request.POST.copy()

        post['day_slug'] = request_data['day_slug']
        post['todo'] = request_data['todo']
        post['sess'] = request.session.session_key

        form_add_todo = AddTodoSerializer(data=post)

        if form_add_todo.is_valid():
            ust = UserSessionToDo(request)
            print(ust.todo_days)
            ust.add_todo(post['todo'], post['day_slug'])
            return Response({'success': True,
                             'message': f'Successfully create {request_data}.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form_add_todo.errors, status=status.HTTP_400_BAD_REQUEST)

    today = get_today().isoformat()
    # Если нет дня, то берем день сегодня
    day = ust.get_obj(kwargs.get('slug_day', today))
    # Берем текущий месяц и год
    day_datetime = get_date(day['slug'])
    cal = MyCalendar(day_datetime.year, day_datetime.month, ust)
    html_cal = cal.formatmonth(withyear=True)
    next_m = navigate_month(day_datetime)
    prev_m = navigate_month(day_datetime, prev=True)
    today_day = {'slug': today}
    context = {'cal': mark_safe(html_cal),
               'day': day,
               'form_add_todo': form_add_todo.data,
               'next_m': next_m,
               'prev_m': prev_m,
               'today_day': today_day,
               'style_btn1': 'btn btn-outline-dark',
               }
    return Response(context, status.HTTP_200_OK)
    # return render(request, 'resume/todo_session.html', context)


@api_view(['DELETE', 'PATCH'])
def TodoDelReplaceSessionViewAPI(request, **kwargs):
    ust = UserSessionToDo(request)
    post_data = request.data
    if request.method == "DELETE":
        todo_del = post_data['del']
        # ust.replace_del(kwargs['slug_day'], todo_del)
        try:
            ust.replace_del(post_data['day'], todo_del)
        except:
            return Response({'message': 'Incorrect data.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'success': True,
                         'message': f'Successfully delete {post_data}.'
                         }, status=status.HTTP_204_NO_CONTENT)


    elif request.method == "PATCH":
        todo_replace = post_data['replace']
        try:
            ust.replace_del(post_data['day'], todo_replace, rep=True)
        except:
            return Response({'message': 'Incorrect data.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'success': True,
                         'message': f'Successfully delete {post_data}.'
                         }, status=status.HTTP_200_OK)
