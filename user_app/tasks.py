import os
from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives, get_connection





@shared_task
def user_delete():
    from user_app.models import Profile
    from django.contrib.auth.models import User
    current_time = timezone.now()
    interval = timezone.timedelta(minutes=1)
    profiles = Profile.objects.filter(Q(create__lte=current_time - interval), ~Q(user__is_staff=True))
    User.objects.filter(profile__in=profiles).delete()


@shared_task
def password_reset_send_mail_task(subject, body, from_email, to_email, html_email_template_name, settings_db,
                                  html_email=None, ):
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

    if html_email:
        email_message.attach_alternative(html_email, 'text/html')

    try:
        email_message.connection = get_connection(
            backend=settings_db['backend'],
            host=settings_db['host'],
            port=settings_db['port'],
            username=settings_db['username'],
            password=settings_db['password'],
            use_tls=settings_db['use_tls']
        )
        email_message.send()
    except Exception as e:
        import traceback
        traceback.print_exc()
