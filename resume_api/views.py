from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from resume.tasks import send_email_task
from resume.cache import count_send_email
from resume.models import AboutMe, MyEducation, Stack
from resume.views import get_ip
from user_app.user_session import UserSessionEmail
from .serializers import AboutMeSerializer, MyEducationSerializer, StackSerializer, FeedbackSerializer, \
    EmailSendSerializer


@api_view(['GET'])
def resume_api(request):
    context = {}
    about_me = AboutMe.objects.all().first()
    if about_me:
        context['about_me'] = AboutMeSerializer(about_me).data
    my_education = MyEducation.objects.all().order_by('-percent')
    context['my_education'] = MyEducationSerializer(my_education, many=True).data
    stacks = Stack.objects.all()
    context['stacks'] = StackSerializer(stacks, many=True).data
    return Response(context, status=status.HTTP_200_OK)


@api_view(['POST'])
def feedback_api(request):
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


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
