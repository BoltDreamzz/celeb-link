from django.apps import AppConfig


class SmmboostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smmboost'

    def ready(self):
        import smmboost.signals
