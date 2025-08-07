from django.apps import AppConfig

class StuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stu_app'

    def ready(self):
        import stu_app.signals