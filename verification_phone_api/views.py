import string
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404 as api404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import (UserRegisterSerializer,
                          ProfileUserSerializer,
                          InviteUserSerializer,
                          PhoneNumberCodeSerializer)
import time
import random
from rest_framework.response import Response
from .cache import get_or_create_number
from .models import CustomUser
from core.settings import ALLOWED_HOSTS
from django.urls import reverse
from .swagger.swagger_descriptions import send_code_verification_schema, invite_code_verification_schema, profile_get, \
    profile_put

host = "http://" + ALLOWED_HOSTS[1]


def generator_invite():
    characters = string.digits + string.ascii_letters
    invite_code = ''.join(random.choice(characters) for _ in range(6))
    return invite_code


@swagger_auto_schema(request_body=PhoneNumberCodeSerializer, **send_code_verification_schema())
@api_view(['POST'])
def send_code_verification(request):
    """
    Получение кода для регистрации user по номеру телефона.

    - Вносим phone_number в body

    """
    serializer = PhoneNumberCodeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        phone_number = serializer.validated_data['phone_number']
        time.sleep(random.uniform(1, 2))
        code = random.randint(1000, 9999)
        get_or_create_number(phone_number, code)
        data = {'code': code}
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(request_body=UserRegisterSerializer, **invite_code_verification_schema())
@api_view(['POST'])
def invite_code_verification(request):
    """
    Заносим в базу данных user и выдаем invite.

    - Вносим в body phone_number и code

    """
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        phone_number = serializer.validated_data['phone_number']
        user = CustomUser.objects.create(
            phone_number=phone_number,
            self_invite=generator_invite()
        )
        data = {'invite': user.self_invite}
        profile_url = reverse('verification_phone_api:profile', args=[user.phone_number])
        data['user_profile_url'] = host + profile_url
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUser(APIView):

    @swagger_auto_schema(**profile_get())
    def get(self, request, *args, **kwargs):
        """

        Полученные данных профиля по номеру телефона

        - Вносим phone_number в path

        """
        phone_number = kwargs.get('phone_number')
        user = api404(CustomUser, phone_number=phone_number)
        all_invite = CustomUser.objects.filter(invite=user.self_invite).exclude(
            phone_number=user.phone_number).values_list('phone_number', flat=True)

        data = {
            "profile": ProfileUserSerializer(user).data,
            'duplicate_user_invite': all_invite
        }

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=InviteUserSerializer, **profile_put())
    def put(self, request, *args, **kwargs):
        """
        Внесение  invite

        - Вносим phone_number в path и invite в body

        """
        phone_number = kwargs.get('phone_number')
        user = api404(CustomUser, phone_number=phone_number)

        if user.is_active:
            data = {"message": "User already activate invite"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = InviteUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.invite = serializer.validated_data['invite']
            user.is_active = True
            user.save()
            data = {"message": f"{user} successfully activated invite"}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
