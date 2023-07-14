from django.apps import AppConfig


from django.conf import settings

class ResumeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resume'
    verbose_name = 'Резюме'



    def ready(self):
        import resume.signals
