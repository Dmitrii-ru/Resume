from rest_framework import serializers
import re

from verification_phone_api.cache import get_number
from verification_phone_api.models import CustomUser

reg_phone_number = re.compile(r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$')


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=16, required=True)
    code = serializers.CharField(min_length=4, max_length=4, required=True)

    def __init__(self, *args, **kwargs):
        include_code = kwargs.pop('include_code', False)
        super().__init__(*args, **kwargs)
        if not include_code:
            self.fields.pop('code')

    def validate_phone_number(self, value):
        phone_number = value
        if not reg_phone_number.match(phone_number):
            raise serializers.ValidationError('Invalid number')
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Not unique number')
        elif not get_number(phone_number):
            raise serializers.ValidationError('This number did not receive a code')
        return value

    def validate_code(self, value):
        code = value
        phone_number = self.initial_data.get('phone_number')
        cache_code = get_number(phone_number)

        if not cache_code:
            raise serializers.ValidationError('Invalid code')
        elif str(code) != str(cache_code):
            raise serializers.ValidationError(f'Request a new code')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'invite', 'self_invite', 'is_active')


class InviteUser(serializers.Serializer):
    invite = serializers.CharField()

    def validate(self, values):
        all_invite = CustomUser.objects.all().values_list('self_invite', flat=True)
        if values['invite'] not in all_invite:
            raise serializers.ValidationError('Invalid invite')
        return values
