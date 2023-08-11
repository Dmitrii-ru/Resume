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
from django.urls import reverse

host = "http://" + ALLOWED_HOSTS[1]


def generator_invite():
    characters = string.digits + string.ascii_letters
    invite_code = ''.join(random.choice(characters) for _ in range(6))
    return invite_code


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, format='+7(929)927-19-00',
                                           example='+7(929)927-19-00'),
        },
        required=['phone_number', ]
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'code': openapi.Schema(type=openapi.TYPE_STRING, example='6666'),
                }
            )
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Validation Error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'object': openapi.Schema(type=openapi.TYPE_STRING, example='phone_number'),
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Not unique number')
                }
            )
        )
    }
)
@api_view(['POST'])
def send_code_verification(request):
    """
    Получение кода для регистрации user по номеру телефона.


    Проверяем формат номера телефона, и наличие телефона в базе данных.

    Кешируем номер телефона и присваиваем код.



    """
    serializer = PhoneNumberSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        phone_number = serializer.validated_data['phone_number']
        time.sleep(random.uniform(1, 2))
        code = random.randint(1000, 9999)
        get_or_create_number(phone_number, code)
        data = {'code': code}
        return Response(data, status=status.HTTP_200_OK)

    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, format='+7(929)927-19-00',
                                           example='+7(929)927-19-00'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, format='1111', example='6839')
        },
        required=['phone_number', 'code']
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'invite': openapi.Schema(type=openapi.TYPE_STRING, example='sYKnvY'),
                    'user_profile_url': openapi.Schema(
                        type=openapi.TYPE_STRING, example='https://host/api/verification_phone/profile/+7(929)927-19-00'
                    )
                }
            )
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Validation Error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'object': openapi.Schema(type=openapi.TYPE_STRING, example='phone_number'),
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Not unique number')
                }
            )
        )
    }
)
@api_view(['POST'])
def invite_code_verification(request):
    """
    Заносим в базу данных user и выдаем invite.


    Проверяем формат номера телефона и наличие телефона в базе данных.

    Берем из кеш номер телефона и проверяем соответствие кода.

    Сохраняем в базе данных, присваиваем invite.


    """
    serializer = PhoneNumberSerializer(data=request.data, include_code=True)
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


class ProfileUser(APIView):
    """
    Работа с профилем


    PUT
    В path вносим phone_number.

    Проверим на существование invite и активировал ли user invite.

    Активируем invite, is_active = true.



    GET
    В path вносим номер телефона
    Запрос:
        {
            Не каких данных не вносим
        }
    Проверим существование номера телефона в базе данных.
    Берем информацию о user.
    Фильтруем users кто применил invite user, за исключением user


    """

    @swagger_auto_schema(
        description='description of param',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'profile': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={
                                "phone_number": "+7(929)924-19-00",
                                "invite": "mrITZ7",
                                "self_invite": "mrITZ7",
                                "is_active": "true"
                            }
                        ),
                        'duplicate_user_invite': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(  # Вот здесь добавили атрибут items
                                type=openapi.TYPE_STRING,
                                example="+7(929)924-19-01"
                            )
                        )
                    }
                )
            ),
        }
    )
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
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='+7(123)456-68-90 успешно активировал invitee'
                        ),
                    }
                )
            ),
        }
    )
    def put(self, request, *args, **kwargs):
        phone_number = kwargs.get('phone_number')
        user = api404(CustomUser, phone_number=phone_number)

        if user.is_active:
            data = {"message": "User already activate invite"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = InviteUser(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.invite = serializer.validated_data['invite']
            user.is_active = True
            user.save()

        data = {"message": f"{user} successfully activated invite"}
        return Response(data, status=status.HTTP_200_OK)
