from django.apps import AppConfig


class TourPackagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tour_packages"

    def ready(self):
        from . import translation  # noqa: F401
