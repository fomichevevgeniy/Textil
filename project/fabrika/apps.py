from django.apps import AppConfig


class FabrikaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fabrika'
    verbose_name = 'Процесс производства'

    def ready(self):
        import fabrika.signals