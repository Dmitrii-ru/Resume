from datetime import date
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from django.utils.safestring import mark_safe
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
import json
from resume.python_prog.calendar_session_todo import MyCalendar
from resume.tasks import send_email_task
from resume.cache import count_send_email, get_model_all, get_single_model_obj, get_filter_model, get_model_all_order, \
    get_mtm_all
from resume.models import AboutMe, MyEducation, Stack, Project, CardProject
from resume.views import get_ip
from user_app.user_session import UserSessionEmail, UserSessionToDo, get_today, get_date, navigate_month
from .serializers import AboutMeSerializer, MyEducationSerializer, StackSerializer, FeedbackSerializer, \
    EmailSendSerializer, ProductSerializer, AddTodoSerializer, TodoDeleteSessionSerializer, TodoPatchSessionSerializer, \
    CardProjectSerializer


@api_view(['GET'])
def resume_api(request):
    """
    Get data index page Resume.
    ---

    """
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
    """
    Send email

    GET - will receive stacks , how many emails can you send, and can you send email.
    POST - send email.

    """
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


def get_date_format(day):
    year, month, day = (int(x) for x in day.split('-'))
    return date(year, month, day).isoformat()


@swagger_auto_schema(method='post', request_body=AddTodoSerializer)
@api_view(['POST', 'GET'])
def TodoSessionViewAPI(request, **kwargs):
    ust = UserSessionToDo(request)
    form_add_todo = AddTodoSerializer()
    try:
        get_date_format(kwargs['slug_day'])
    except:
        return Response({'success': False,
                         'message': f'Format YYYY-MM-DD != {kwargs["slug_day"]}.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        request_data = request.data
        form_add_todo = AddTodoSerializer(data=request_data, context={'ust': ust, 'day': kwargs['slug_day']})

        if form_add_todo.is_valid():
            ust = UserSessionToDo(request)
            ust.add_todo(request_data['todo'], kwargs['slug_day'])
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


@swagger_auto_schema(method='DELETE', request_body=TodoDeleteSessionSerializer,
                     manual_parameters=[
                         openapi.Parameter(name='slug_day',
                                           in_=openapi.IN_PATH,
                                           type=openapi.TYPE_STRING,
                                           description=f"Format YYYY-MM-DD"),
                     ])
@api_view(['DELETE'])
def TodoDeleteSessionViewAPI(request, **kwargs):
    ust = UserSessionToDo(request)
    data = TodoDeleteSessionSerializer()
    if request.method == "DELETE":
        post_data = request.data

        delete_form = TodoDeleteSessionSerializer(data=post_data, context={'ust': ust, 'slug_day': kwargs['slug_day']})
        if delete_form.is_valid():
            try:
                ust.del_todo_api(kwargs['slug_day'], post_data['status_todo'], post_data['todo'])
            except:
                return Response({'message': 'Incorrect data.'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'success': True,
                             'message': f'Successfully delete {post_data}.'
                             }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(delete_form.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status.HTTP_200_OK)


@swagger_auto_schema(method='PATCH', request_body=TodoPatchSessionSerializer,
                     manual_parameters=[
                         openapi.Parameter(name='slug_day',
                                           in_=openapi.IN_PATH,
                                           type=openapi.TYPE_STRING,
                                           description=f"Format YYYY-MM-DD"),
                     ])
@api_view(['PATCH'])
def TodoPatchSessionViewAPI(request, **kwargs):
    ust = UserSessionToDo(request)
    data = TodoPatchSessionSerializer()

    if request.method == "PATCH":
        post_data = request.data
        patch_form = TodoPatchSessionSerializer(data=post_data, context={'ust': ust, 'day': kwargs['slug_day']})
        if patch_form.is_valid():
            try:
                ust.patch_todo_api(kwargs['slug_day'], post_data['new_status_todo'], post_data['todo'])
            except:
                return Response({'message': 'Incorrect data.'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'success': True,
                             'message': f'Successfully delete {post_data}.'
                             }, status=status.HTTP_200_OK)
        else:
            return Response(patch_form.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)


class ProjectsAPIReadOnly(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_summary="Get projects",
        operation_description="We receive projects using slug technology.",
        manual_parameters=[
            openapi.Parameter(
                name="stack_slug",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description=f"Slug of the stack, you can use this data: "
                            f"{list(get_model_all(Stack).values_list('slug', flat=True))}",
                required=True,
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        data = {'projects': self.get_serializer(get_filter_model(
            Project,
            'stacks__slug',
            self.kwargs['stack_slug']), many=True).data,

                'stacks': StackSerializer(get_model_all(Stack), many=True).data,
                'stack': StackSerializer(get_single_model_obj(Stack, 'slug', self.kwargs['stack_slug'])).data}
        return Response(data)


class ProjectDetailAPIReadOnly(ReadOnlyModelViewSet):
    serializer_class = CardProjectSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'stack_slug',
                openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description=f"Selector {list(get_model_all(Stack).values_list('slug', flat=True))}",
                required=True,
            ),
            openapi.Parameter(
                'project_slug',
                openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description=f"Selector {list(get_model_all(Project).values_list('slug', flat=True))}",
                required=True,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        data = {}
        projects = get_filter_model(Project, 'stacks__slug', self.kwargs['stack_slug'])

        try:
            project = get_object_or_404(projects, slug=self.kwargs['project_slug'])
        except Http404:
            return HttpResponse(f'Project with slug "{self.kwargs["project_slug"]}" '
                                f'not found in technology with slug "{self.kwargs["stack_slug"]}"', status=404)
        data['project'] = ProductSerializer(project).data
        data['cards'] = self.get_serializer(get_filter_model(CardProject, 'project', project), many=True).data
        data['stacks'] = StackSerializer(get_mtm_all(Project, 'stacks', project), many=True).data
        return Response(data, status=status.HTTP_200_OK)
