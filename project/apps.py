from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "project"  # Name of the app

    def ready(self):
        import project.signals  # Import signals module to handle events
