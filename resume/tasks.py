from datetime import timedelta
from celery import shared_task
from core.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT
from resume.python_prog.send_mail_prog import send_email_my
from django.utils import timezone

import django
django.setup()

from resume.models import EmailSend


sender = EMAIL_HOST_USER
password = EMAIL_HOST_PASSWORD



@shared_task
def send_email_task(massage=None, to_send=None, name=None, host=None, subject=None, session_id=None):

    try:
        send_email_my(massage, to_send, name, host, subject, session_id)
        return 'Your massage was send successfully!'
    except Exception as error:
        return f"{error} Check your password or login"

@shared_task
def check_email_old_task():
    print('check_email_old_task')
    three_days_ago = timezone.now() - timedelta(days=3)
    old_mails = EmailSend.objects.filter(date__lt=three_days_ago)
    if old_mails:
        for obj in old_mails:
            massage = f'{obj.name}, жду от Вас положительно ответа,мое резюме {"ТУТ ДОЛЖНА БЫТЬ ССЫЛКА НА САЙТ"}'
            subject = 'Непомнине от соискателя'
            send_email_task.delay(massage=massage, to_send=obj.email, subject=subject)
        old_mails.delete()
