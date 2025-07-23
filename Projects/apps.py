from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Projects'
    verbose_name = "Real Estate Projects"
    
    def ready(self):
        # Import admin here to ensure all models are registered
        from . import admin
