from rest_framework import serializers, status
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.response import Response

from resume.forms import reg
from resume.models import AboutMe, MyEducation, Stack, Feedback, EmailSend, Project
import re

from user_app.user_session import UserSessionToDo, get_date_format


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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
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

    def validate_email(self, value):
        if not re.match(reg, value):
            raise serializers.ValidationError('Email is not correct')
        return value

    def validate_name(self, value):
        if len(value) < 2 or any(map(str.isdigit, value)):
            raise serializers.ValidationError('Short name')
        return value.title()


class AddTodoSerializer(serializers.Serializer):
    todo = serializers.CharField(max_length=20)
    day_slug = serializers.CharField()
    sess = serializers.CharField()

    def validate(self, values):
        ust = UserSessionToDo(SessionStore(values['sess']), sess=True)
        try:
            get_date_format(values['day_slug']).isoformat()
        except:
            raise serializers.ValidationError('Format YYYY-MM-DD')

        day = ust.todo_days.get(values['day_slug'], ust.new_obj(values['day_slug']))
        print(day.items())
        todo = values['todo']

        try:
            if todo in day['actual'] or todo in day['close']:
                raise serializers.ValidationError(f"Already is tasks fot today")
        except:
            raise serializers.ValidationError(f"Many keys {todo}")

        if len(todo) < 2:
            raise serializers.ValidationError('The "todo" field must have a length greater than 2.')
        elif len(todo) > 20:
            raise serializers.ValidationError('The "togo" no more than 20 characters')
        print(day)
        print(ust.todo_days)

        return values
