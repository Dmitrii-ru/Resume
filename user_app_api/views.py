from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, User, RefreshTokenSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .swagger.swagger_descriptions import schema_login, schema_refresh_token, schema_user_register
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404 as api404


class UserRegisterAPIView(CreateAPIView):
    """
    Регистрация пользователя


    """

    @swagger_auto_schema(request_body=UserRegistrationSerializer, **schema_user_register())
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user = {
            'username': user.username,
            'email': user.email,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

        return Response(user, status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    Аутентификация пользователя


    """

    @swagger_auto_schema(request_body=UserLoginSerializer, **schema_login())
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data['username']
            password = request.data['password']
            user = api404(User, username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('Invalid password')
            elif not user.is_active:
                raise serializers.ValidationError('User not active')

            refresh = RefreshToken.for_user(user)
            data = {
                'user': user.username,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    """
    Обновление токенов


    """

    @swagger_auto_schema(request_body=RefreshTokenSerializer, **schema_refresh_token())
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh_token']
            try:
                refresh = RefreshToken(refresh_token)
                access_token = str(refresh.access_token)
            except Exception as e:
                return Response({'error': f'Bad refresh_token ({e})'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'access_token': access_token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
