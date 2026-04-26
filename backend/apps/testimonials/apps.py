from django.apps import AppConfig


class TestimonialsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.testimonials"

    def ready(self):
        from . import translation  # noqa: F401
