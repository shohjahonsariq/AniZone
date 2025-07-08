from django.apps import AppConfig

class AppNameConfig(AppConfig):  # ✅ SENING APPING NOMIDAN QO‘YILGAN NOM
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals
