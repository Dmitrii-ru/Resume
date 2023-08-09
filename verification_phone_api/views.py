import string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404 as api404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import PhoneNumberSerializer, CustomUserSerializer, InviteUser
import time
import random
from rest_framework.response import Response
from .cache import get_or_create_number
from .models import CustomUser
from core.settings import ALLOWED_HOSTS
host = "http://" + ALLOWED_HOSTS[1]
def generator_invite():
    characters = string.digits + string.ascii_letters
    invite_code = ''.join(random.choice(characters) for _ in range(6))
    return invite_code


@swagger_auto_schema(method='post', request_body=PhoneNumberSerializer(default={'phone_number': '+7(123)456-78-90'}))
@api_view(['POST'])
def send_code_verification(request):
    """
    Получение кода для регистрации user по номеру телефона.

    Endpoint api/verification_phone/send_code_verification
    Запрос:
    {
        "phone_number": "+7(929)927-19-00"
    }

    Проверяем формат номера телефона, и наличие телефона в базе данных.
    Кешируем номер телефона и его код.
    time.sleep(random.uniform(1, 2))
    Ответ:
    {
        "code": 3429
    }


    """
    form = PhoneNumberSerializer(data=request.data)
    if form.is_valid(raise_exception=True):
        phone_number = form.validated_data['phone_number']
        time.sleep(random.uniform(1, 2))
        code = random.randint(1000, 9999)
        get_or_create_number(phone_number, code)
        data = {'code': code}
        return Response(data, status=status.HTTP_200_OK)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',

    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, format='+7(929)927-19-00',
                                           example='+7(929)927-19-37'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, format='1111', example='6839')
        },
        required=['phone_number', 'code']
    )
)
@api_view(['POST'])
def invite_code_verification(request):
    """
    Заносим в базу данных user и выдаем invite.

    Endpoint api/verification_phone/invite_code_verification
    Запрос:
        {
          "phone_number": "+7(929)927-19-00",
          "code": "6839"
        }
    Проверяем формат номера телефона, и наличие телефона в базе данных.
    Берем из кеш номер телефон и проверяем соответствие кода.
    Сохраняем в базе данных, присваиваем invite.

    Ответ:
        {
            "invite": "sYKnvY"
        }

    """
    form = PhoneNumberSerializer(data=request.data, include_code=True,
                                 )
    if form.is_valid(raise_exception=True):
        phone_number = form.validated_data['phone_number']
        user = CustomUser.objects.create(
            phone_number=phone_number,
            self_invite=generator_invite()
        )
        data = {'invite': user.self_invite}
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(form.data, status=status.HTTP_200_OK)


class ProfileUser(APIView):
    """
    Работа с профилем

    Endpoint api/verification_phone/profile/<phone_number>
    POST
    В path вносим phone_number.
    Запрос:
        {
          "invite": "string"
        }
    Проверим на существование invite и активировал ли user invite.

    Активируем invite, is_active = true.

    Ответ:
        {
          "message": "+7(123)456-68-90 успешно активировал invitee"
        }


    GET
    В path вносим номер телефона
    Запрос:
        {
            Не каких данных не вносим
        }
    Проверим существование номера телефона в базе данных.
    Берем информацию о user.
    Фильтруем users кто применил invite user, за исключением user

    Ответ:
        {
            "message": "Profile user ",
            "profile": {
                "id": 5,
                "phone_number": "+7(929)927-19-00",
                "invite": "Aw1bO6",
                "self_invite": "Aw1bO6",
                "is_active": true
            },
            "duplicate_user_invite": [
                "+7(929)927-19-77"
            ]
        }


    """

    def get(self, request, *args, **kwargs):
        phone_number = kwargs.get('phone_number')
        user = api404(CustomUser, phone_number=phone_number)
        all_invite = CustomUser.objects.filter(invite=user.self_invite).exclude(
            phone_number=user.phone_number).values_list('phone_number', flat=True)

        data = {
            "profile": CustomUserSerializer(user).data,
            'duplicate_user_invite': all_invite
        }

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=InviteUser,

    )
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

        data = {"message": f"{user} успешно активировал invite"}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
