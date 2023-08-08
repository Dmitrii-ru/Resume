import string

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import PhoneNumberSerializer
import time
import random
from rest_framework.response import Response
from .cache import get_or_create_number
from .models import CustomUser


def generator_invite():
    characters = string.digits + string.ascii_letters
    invite_code = ''.join(random.choice(characters) for _ in range(6))
    return invite_code


@api_view(['POST'])
def send_code_verification(request):
    form = PhoneNumberSerializer(data=request.data)
    if form.is_valid(raise_exception=True):
        phone_number = form.validated_data['phone_number']
        time.sleep(random.uniform(1, 2))
        code = random.randint(1000, 9999)
        get_or_create_number(phone_number, code)
        return Response({
            'success': True,
            'message': f'Смс {get_or_create_number(phone_number, code)} на номер {phone_number}. Код: {code}.'
        }, status=status.HTTP_201_CREATED)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def invite_code_verification(request):
    form = PhoneNumberSerializer(data=request.data, include_code=True,
                                 context={'phone_number': request.data['phone_number']})
    if form.is_valid(raise_exception=True):
        phone_number = form.validated_data['phone_number']

        custom_user, created = CustomUser.objects.get_or_create(
            phone_number=phone_number, defaults={
                'self_invite': generator_invite()
            }
        )
        if created:
            return Response({
                'success': True,
                'message': f'Пользователь {custom_user.phone_number} успешно создан, Ваш инвайт пароль {custom_user.self_invite}'
            }, status=status.HTTP_201_CREATED)

    Response(form.data, status=status.HTTP_200_OK)
