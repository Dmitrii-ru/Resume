import os

from celery import shared_task
from django.db.models import Q
from django.utils import timezone

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from user_app.models import Profile
from django.contrib.auth.models import User

@shared_task
def user_delete():
    print('user_delete')
    current_time = timezone.now()
    interval = timezone.timedelta(minutes=15)
    profiles = Profile.objects.filter(Q(create__lte=current_time - interval), ~Q(user__is_staff=True))
    User.objects.filter(profile__in=profiles).delete()





