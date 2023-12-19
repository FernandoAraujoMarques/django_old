from django.apps import AppConfig

class LucrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lucros'

    def ready(self):
        import lucros.signals
