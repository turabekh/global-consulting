from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    class Language(models.TextChoices):
        UZBEK = "uz", _("Uzbek")
        ENGLISH = "en", _("English")
        RUSSIAN = "ru", _("Russian")
        SPANISH = "es", _("Spanish")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(_("bio"), blank=True)
    language = models.CharField(
        _("language"),
        max_length=8,
        choices=Language.choices,
        default=Language.ENGLISH,
    )
    timezone = models.CharField(_("timezone"), max_length=64, default="UTC")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"Profile of {self.user.email}"
