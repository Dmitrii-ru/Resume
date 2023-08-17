from datetime import date
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from resume.cache import get_model_all, get_single_model_obj, get_filter_model, get_model_all_order, \
    get_mtm_all
from resume.models import AboutMe, MyEducation, Stack, Project, CardProject
from user_app.user_session import UserSessionToDo
from .serializers import AboutMeSerializer, MyEducationSerializer, StackSerializer, FeedbackSerializer, \
    ProductSerializer, AddTodoSerializer, TodoDeleteSessionSerializer, TodoPatchSessionSerializer, \
    CardProjectSerializer
from .swagger.swagger_descriptions import schema_index, schema_feedback


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


def get_date_format(day):
    year, month, day = (int(x) for x in day.split('-'))
    return date(year, month, day).isoformat()


def get_or_create_day(ust, day_d):
    day = ust.todo_days.get(day_d)
    if not day:
        day = ust.new_obj(day_d)
    return day


@swagger_auto_schema(method='post', request_body=AddTodoSerializer)
@api_view(['POST', 'GET'])
def todo_session_view_api(request, **kwargs):
    """
    Get or create todo_.

    Create a new feedback object by providing the text in the request body.

    ---

    """

    ust = UserSessionToDo(request)

    try:
        get_date_format(kwargs['slug_day'])
    except ValueError:
        return Response(
            {
                'success': False,
                'error': f'Invalid date format. Please provide a valid date in YYYY-MM-DD format.'
            }, status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == "POST":
        request_data = request.data
        day = ust.todo_days.get(kwargs['slug_day'])
        serializer = AddTodoSerializer(data=request_data)

        if day:
            serializer = AddTodoSerializer(data=request_data, context={'day': day})
        else:
            ust.new_obj(kwargs['slug_day'])

        if serializer.is_valid():
            ust = UserSessionToDo(request)
            ust.add_todo(serializer.validated_data['todo'], kwargs['slug_day'])
            return Response(
                {
                    'success': True,
                    'message': f'Successfully create todo.'
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = {'day': ust.get_obj(kwargs['slug_day'])}
    return Response(data, status.HTTP_200_OK)


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
