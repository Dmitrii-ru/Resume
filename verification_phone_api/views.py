import string

from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404 as api404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import PhoneNumberSerializer, reg_phone_number, CustomUserSerializer
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
        if not reg_phone_number.match(phone_number):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = api404(CustomUser, phone_number=phone_number)
        all_invite = CustomUser.objects.all().values_list('self_invite', flat=True)

        data = {"message": "This is a GET request", 'all_invite': all_invite}
        data["profile_user"] = CustomUserSerializer(user)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {"message": "This is a POST request"}
        return Response(data, status=status.HTTP_201_CREATED)
