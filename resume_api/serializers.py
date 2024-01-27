from datetime import date

from rest_framework import serializers, status
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.response import Response

from resume.forms import reg
from resume.models import AboutMe, MyEducation, Stack, Feedback, EmailSend, Project, CardProject
import re

from user_app.user_session import UserSessionToDo


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


class CardProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardProject
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        min_length=10,
    )

    class Meta:
        model = Feedback
        fields = ('text',)


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


def get_or_create_day(ust, day_d):
    day = ust.todo_days.get(day_d)
    if not day:
        day = ust.new_obj(day_d)
    return day


def get_date_format(day):
    year, month, day = (int(x) for x in day.split('-'))
    return date(year, month, day).isoformat()


class AddTodoSerializer(serializers.Serializer):
    todo = serializers.CharField(
        max_length=20,
        min_length=2,
    )

    def validate_todo(self, value):
        todo = value
        day = self.context.get('day')
        if day:
            if todo in day['actual']:
                raise serializers.ValidationError(f"The todo already exists in actual")
            elif todo in day['close']:
                raise serializers.ValidationError(f"The todo already exists in close")
        return value


class TodoDeletePutSerializer(serializers.Serializer):
    todo = serializers.CharField(
        min_length=2,
        max_length=20
    )

    def validate_todo(self, value):
        todo = value
        day = self.context.get('day')
        if todo not in day['close'] and todo not in day['actual']:
            raise serializers.ValidationError(f"The todo does not exists")
        return value




class TodoPatchSessionSerializer(serializers.Serializer):
    todo = serializers.CharField(max_length=20)
    new_status_todo = serializers.CharField(max_length=10)

    def validate(self, values):
        todo = values['todo']
        new_status_todo = values['new_status_todo']
        selector = ['actual', 'close']
        ust = self.context.get('ust')
        slug_day = self.context.get('day')

        try:
            get_date_format(slug_day)
        except:
            raise serializers.ValidationError(f'Format {slug_day} !=  YYYY-MM-DD ')

        if not ust.todo_days.get(slug_day):
            raise serializers.ValidationError(f'There are no tasks {slug_day}')

        elif new_status_todo not in selector:
            raise serializers.ValidationError(f'Select status {selector}')

        else:
            selector.remove(new_status_todo)

            if todo not in ust.todo_days[slug_day][selector[0]]:
                raise serializers.ValidationError(f'No such task {todo} in {selector[0]} ({slug_day})')

        return values
