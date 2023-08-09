import string
from django.db.models import Prefetch, Exists, OuterRef
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404 as api404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import PhoneNumberSerializer, reg_phone_number, CustomUserSerializer, InviteUser
import time
import random
from rest_framework.response import Response
from .cache import get_or_create_number
from .models import CustomUser


def generator_invite():
    characters = string.digits + string.ascii_letters
    invite_code = ''.join(random.choice(characters) for _ in range(6))
    return invite_code


@swagger_auto_schema(method='post', request_body=PhoneNumberSerializer)
@api_view(['POST'])
def send_code_verification(request):
    form = PhoneNumberSerializer(data=request.data)
    if form.is_valid(raise_exception=True):
        phone_number = form.validated_data['phone_number']
        time.sleep(random.uniform(1, 2))
        code = random.randint(1000, 9999)

        return Response({
            'success': True,
            'message': f'Смс {get_or_create_number(phone_number, code)} на номер {phone_number}. Код: {code}.'
        }, status=status.HTTP_201_CREATED)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=PhoneNumberSerializer)
@api_view(['POST'])
def invite_code_verification(request):
    form = PhoneNumberSerializer(data=request.data, include_code=True,
                                 )
    if form.is_valid(raise_exception=True):
        phone_number = form.validated_data['phone_number']
        custom_user = CustomUser.objects.create(
            phone_number=phone_number,
            self_invite=generator_invite()
        )
        return Response({
            'success': True,
            'message': f'Пользователь {custom_user.phone_number} '
                       f'успешно создан, Ваш инвайт пароль :{custom_user.self_invite}'
        }, status=status.HTTP_201_CREATED)

    return Response(form.data, status=status.HTTP_200_OK)


class ProfileUser(APIView):
    def get(self, request, *args, **kwargs):
        phone_number = kwargs.get('phone_number')

        user = api404(CustomUser, phone_number=phone_number)
        all_invite = CustomUser.objects.filter(invite=user.self_invite).exclude(phone_number=user.phone_number).values_list('phone_number', flat=True)

        data = {"message": f"Profile user ",
                "profile": CustomUserSerializer(user).data,
                'duplicate_user_invite': all_invite
                }

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        phone_number = kwargs.get('phone_number')
        user = api404(CustomUser, phone_number=phone_number)

        if user.is_active:
            data = {"message": "User already activate invite"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        form = InviteUser(data=request.data)
        if form.is_valid(raise_exception=True):
            user.invite = form.validated_data['invite']
            user.is_active = True
            user.save()

        data = {"message": f"{user} successfully activate invite"}
        return Response(data, status=status.HTTP_201_CREATED)
