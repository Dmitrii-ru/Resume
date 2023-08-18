from datetime import date
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from resume.cache import get_model_all, get_single_model_obj, get_filter_model, get_model_all_order, \
    get_mtm_all
from resume.models import AboutMe, MyEducation, Stack, Project, CardProject
from user_app.user_session import UserSessionToDo
from .serializers import AboutMeSerializer, MyEducationSerializer, StackSerializer, FeedbackSerializer, \
    ProductSerializer, AddTodoSerializer, TodoPatchSessionSerializer, \
    CardProjectSerializer, TodoDeleteSerializer
from .swagger.swagger_descriptions import *


@swagger_auto_schema(method='get', **schema_index())
@api_view(['GET'])
def resume_api(request):
    """
    Get person's skills.

    Get information about a person's skills , contacts.


    ---

    """
    data = {}
    about_me = get_model_all(AboutMe)
    if about_me:
        data['about_me'] = AboutMeSerializer(about_me[0]).data
    data['my_education'] = MyEducationSerializer(get_model_all_order(MyEducation, '-percent'), many=True).data
    data['stacks'] = StackSerializer(get_model_all(Stack), many=True).data
    data['projects'] = ProductSerializer(get_model_all(Project), many=True).data
    return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=FeedbackSerializer, **schema_feedback())
@api_view(['POST'])
def feedback_api(request):
    """
    Create a new feedback.

    Create a new feedback object by providing the text in the request body.

    ---

    """
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Feedback successfully created'}, status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_day_format(day):
    try:
        year, month, day = (int(x) for x in day.split('-'))
        date(year, month, day).isoformat()

    except ValueError:
        return True


def response_format_day_error():
    return Response(
        {
            'success': False,
            'error': f'Invalid date format. Please provide a valid date in YYYY-MM-DD format.'
        }, status=status.HTTP_400_BAD_REQUEST
    )


class TodoViewApi(APIView):
    @swagger_auto_schema(**schema_todo_get())
    def get(self, request, **kwargs):
        """
        Getting to-do day

        Enter day in params

        """
        slug_day = self.kwargs.get('slug_day')
        if get_day_format(slug_day):
            return response_format_day_error()

        ust = UserSessionToDo(self.request)

        data = {'day': ust.get_obj(slug_day)}
        return Response(data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AddTodoSerializer, **schema_todo_post())
    def post(self, request, **kwargs):
        """

        Create new to-do

        Enter day in params and to-go in body

        """

        slug_day = self.kwargs.get('slug_day')
        if get_day_format(slug_day):
            return response_format_day_error()
        ust = UserSessionToDo(self.request)

        request_data = request.data
        day = ust.todo_days.get(slug_day)

        serializer = AddTodoSerializer(data=request_data)
        if day:
            serializer = AddTodoSerializer(data=request_data, context={'day': day})
        else:
            ust.new_obj(slug_day)

        if serializer.is_valid():
            ust = UserSessionToDo(request)
            ust.add_todo(serializer.validated_data['todo'], slug_day)
            return Response(
                {
                    'success': True,
                    'message': f'Successfully create todo.'
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE', request_body=TodoDeleteSerializer, **schema_todo_delete())
@api_view(['DELETE', 'PUT'])
def todo_delete_api(request, **kwargs):
    """
    Delete to-do or change status to-do

    Enter day in params and to-go in body

    ---

    """

    slug_day = kwargs.get('slug_day')
    if get_day_format(slug_day):
        return response_format_day_error()
    ust = UserSessionToDo(request)

    day = ust.todo_days.get(slug_day)

    if not day:
        return Response(
            {
                'success': False,
                'error': 'Date not found.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TodoDeleteSerializer(data=request.data, context={'day': day})

    if serializer.is_valid():
        method_path = request.path.split('/')[-1]
        todo = serializer.validated_data['todo']
        status_todo = 'close' if todo in day['close'] else 'actual'

        if request.method == 'DELETE' and method_path == 'delete':

            ust.del_todo_api(slug_day, status_todo, todo)
            return Response(
                {
                    'success': True,
                    'message': f"Successfully delete '{todo}'."
                },
                status=status.HTTP_204_NO_CONTENT
            )
        elif request.method == 'PUT' and method_path == 'status':
            new_status = ust.patch_todo_api(slug_day, status_todo, todo)
            return Response(
                {
                    'success': True,
                    'message': f"Successfully change status '{todo}' on {new_status}."
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'success': False,
                    'error': f"Invalid method or endpoint."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PUT', request_body=TodoPatchSessionSerializer,
                     manual_parameters=[
                         openapi.Parameter(name='slug_day',
                                           in_=openapi.IN_PATH,
                                           type=openapi.TYPE_STRING,
                                           description=f"Format YYYY-MM-DD"),
                     ])
@api_view(['PUT'])
def todo_status_put_api(request, **kwargs):
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
