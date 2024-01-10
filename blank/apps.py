from django.apps import AppConfig


class BlankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blank'

    def ready(self):
        import blank.signals