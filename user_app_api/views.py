from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from user_app.models import Profile


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



