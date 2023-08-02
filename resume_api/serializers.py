from rest_framework import serializers

from resume.forms import reg
from resume.models import AboutMe, MyEducation, Stack, Feedback, EmailSend
import re

class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMe
        fields = '__all__'


class MyEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyEducation
        fields = '__all__'


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('text',)

    def validate_text(self, value):
        if not value:
            raise serializers.ValidationError('Write text')
        if len(value) < 10:
            raise serializers.ValidationError('You are very modest, at least 10 characters')
        return value


class EmailSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSend
        fields = ('name', 'email',)

    def validate_email(self,value):
        if not re.match(reg, value):
            raise serializers.ValidationError('Email is not correct')
        return value

    def validate_name(self,value):
        if len(value) < 2 or any(map(str.isdigit, value)):
            raise serializers.ValidationError('Short name')
        return value.title()
