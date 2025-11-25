from django.apps import AppConfig


class OcrAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ocr_system'

    def ready(self):
        import ocr_system.templatetags.basename