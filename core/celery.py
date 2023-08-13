import os
from celery import Celery
import user_app.tasks
import resume.tasks
from celery.schedules import crontab

broker_connection_retry_on_startup = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core', broker='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        59.0,
        user_app.tasks.user_delete.s(),
        name='delete_user'
    ),

    sender.add_periodic_task(
        crontab(hour=0, minute=1),
        resume.tasks.check_email_old_task.s(),
        name='check_old_emails'
    )

    sender.add_periodic_task(
        crontab(hour=0, minute=1),
        resume.tasks.del_ip_all_task.s(),
        name='del_ip_all'
    )

    sender.add_periodic_task(
        crontab(hour=0, minute=1),
        resume.tasks.create_visit_task.s(),
        name='create_visit'
    )

    sender.add_periodic_task(
        8.0,
        resume.tasks.create_visit_task.s(),
        name='create_visit_time'
    )
