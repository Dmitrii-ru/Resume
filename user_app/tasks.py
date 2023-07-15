import os
from django.conf import settings
from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives, get_connection
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from user_app.models import Profile
from django.contrib.auth.models import User


@shared_task
def user_delete():
    print('user_delete_task')
    current_time = timezone.now()
    interval = timezone.timedelta(minutes=15)
    profiles = Profile.objects.filter(Q(create__lte=current_time - interval), ~Q(user__is_staff=True))
    User.objects.filter(profile__in=profiles).delete()


@shared_task
def password_reset_send_mail_task(subject, body, from_email, to_email, html_email_template_name, html_email=None):
    from resume.models import EmailSettings
    email_settings_db = EmailSettings.objects.filter(is_active='True').first()
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

    if html_email:
        email_message.attach_alternative(html_email, 'text/html')

    if email_settings_db:
        try:
            email_message.connection = get_connection(
                backend=settings.EMAIL_BACKEND,
                host=email_settings_db.host_email,
                port=email_settings_db.port_email,
                username=email_settings_db.name_email,
                password=email_settings_db.password_email,
                use_tls=settings.EMAIL_USE_TLS,
            )
            email_message.send()
        except Exception as e:
            import traceback
            traceback.print_exc()

