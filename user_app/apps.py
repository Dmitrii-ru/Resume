from django.apps import AppConfig


class UserappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'
    verbose_name = 'Профиль пользователя'

    def ready(self):
        import user_app.signals
