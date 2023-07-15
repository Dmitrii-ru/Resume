import os
from celery import Celery
import user_app.tasks
import resume.tasks
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        283182.0,
        user_app.tasks.user_delete.s(),
        name='delete_user'
    ),

    sender.add_periodic_task(
        crontab(hour=0, minute=1),
        resume.tasks.check_email_old_task.s(),
        name='check_old_emails'
    )

