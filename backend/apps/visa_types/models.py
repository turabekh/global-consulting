from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class VisaType(models.Model):
    class Category(models.TextChoices):
        TOURIST = "tourist", _("Tourist")
        STUDENT = "student", _("Student")
        WORK = "work", _("Work")
        BUSINESS = "business", _("Business")
        FAMILY = "family", _("Family")

    title = models.CharField(_("title"), max_length=200)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=False)
    country = models.CharField(_("destination country"), max_length=120)
    description = models.TextField(_("short description"), max_length=500, blank=True)
    body = models.TextField(_("body"), help_text=_("Markdown is supported."))
    cover_image = models.ImageField(_("cover image"), upload_to="visa-types/")

    processing_time = models.CharField(
        _("processing time"),
        max_length=120,
        blank=True,
        help_text=_("Free text, e.g. '4-6 weeks'"),
    )
    success_rate = models.PositiveIntegerField(
        _("success rate (%)"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    category = models.CharField(
        _("category"),
        max_length=16,
        choices=Category.choices,
        default=Category.TOURIST,
        db_index=True,
    )

    order = models.PositiveIntegerField(_("order"), default=0)
    is_active = models.BooleanField(_("active"), default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("visa type")
        verbose_name_plural = _("visa types")
        ordering = ("order", "country", "title")

    def __str__(self):
        return f"{self.title} ({self.country})"
