from django.apps import AppConfig


class FaqConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.faq"

    def ready(self):
        from . import translation  # noqa: F401
