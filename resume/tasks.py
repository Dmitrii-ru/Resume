from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from resume.cache import del_ip_all


@shared_task
def send_email_task(massage_num, to_send, name, subject):
    from resume.python_prog.send_mail_prog import send_email_my
    try:
        send_email_my(massage_num, to_send, name, subject)
        return 'Your massage was send successfully!'
    except Exception as error:
        return f"{error} Error"


@shared_task
def check_email_old_task():
    from resume.models import EmailSend
    three_days_ago = timezone.now() - timedelta(days=3)
    old_mails = EmailSend.objects.filter(date__lt=three_days_ago)
    if old_mails:
        for obj in old_mails:
            massage = 2
            subject = 2
            send_email_task.delay(name=obj.name, massage_num=massage, to_send=obj.email, subject=subject)
        old_mails.delete()


@shared_task
def del_ip_all_task():
    del_ip_all()


def create_visit_task():
    import redis
    import json
    from .models import UniqueIP

    db2 = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)
    all_keys = db2.keys()
    create_list = []
    for key in all_keys:
        val = json.loads(db2.get(key))
        create_list.append(
            UniqueIP(
                ip_address=key,
                path_client=val['path_client'],
                info_client=val['info_client'],
            )
        )
    UniqueIP.objects.bulk_create(
        create_list
    )
    db2.flushdb()
