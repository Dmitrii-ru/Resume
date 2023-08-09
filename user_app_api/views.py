from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, User
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework import serializers, status


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'username': user.username,
            'email': user.email,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })


class LoginAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description=f"username",
                required=True,
            ),
            openapi.Parameter(
                'password',
                openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description=f"password",
                required=True,
            ),
        ]
    )
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = User.objects.filter(username=username).first()

            if not user:
                raise serializers.ValidationError('User not found')

            elif not user.check_password(password):
                raise serializers.ValidationError('Invalid password')

            elif not user.is_active:
                raise serializers.ValidationError('User not active')

            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': user.username,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                })
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'refresh_token is required'}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception as e:
            return Response({'error': f'Bad refresh_token ({e})'}, status=400)

        return Response({'access_token': access_token})
