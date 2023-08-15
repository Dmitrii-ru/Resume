from rest_framework import serializers
import re

from verification_phone_api.cache import get_number
from verification_phone_api.models import CustomUser

reg_phone_number = re.compile(r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$')


class PhoneNumberCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        min_length=16,
        required=True,
        help_text='Phone number format: "+7(XXX)XXX-XX-XX", example = "+7(929)927-19-00"'
    )

    def validate_phone_number(self, value):
        phone_number = value
        if not reg_phone_number.match(phone_number):
            raise serializers.ValidationError('Invalid number')
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Not unique number')
        return value


class UserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        min_length=16,
        required=True,
        help_text='Phone number format: "+7(XXX)XXX-XX-XX", example = "+7(929)927-19-00"'
    )

    code = serializers.CharField(
        min_length=4,
        max_length=4,
        required=True,
        help_text='Phone code: "XXXX", example = "1233'

    )

    def validate_phone_number(self, value):
        phone_number = value
        if not reg_phone_number.match(phone_number):
            raise serializers.ValidationError('Invalid number')
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Not unique number')
        return value

    def validate_code(self, value):
        code = value
        phone_number = self.initial_data.get('phone_number')
        cache_code = get_number(phone_number)

        if not cache_code:
            raise serializers.ValidationError('This phone number did not receive a code')
        elif str(code) != str(cache_code):
            raise serializers.ValidationError(f'Request a new code')
        return value


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'invite', 'self_invite', 'is_active')


class InviteUserSerializer(serializers.Serializer):
    invite = serializers.CharField(
        min_length=6,
        max_length=6,
        help_text='"XXXXXX", example = "T5R7uO"'
    )

    class Meta:
        model = CustomUser
        fields = 'invite'

    def validate(self, values):
        all_invite = CustomUser.objects.all().values_list('self_invite', flat=True)
        if values['invite'] not in all_invite:
            raise serializers.ValidationError('Invalid invite')
        return values
