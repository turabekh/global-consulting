from django.apps import AppConfig


class VisaTypesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.visa_types"

    def ready(self):
        from . import translation  # noqa: F401
