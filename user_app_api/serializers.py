from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, values):
        if values['password'] != values['password2']:
            raise serializers.ValidationError('password != password2')
        return values

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        del validated_data['password2']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=20,
        min_length=3,
    )

    password = serializers.CharField(
        max_length=20,
        min_length=3,
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


