from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _


class University(models.Model):
    class Currency(models.TextChoices):
        USD = "USD", "USD"
        EUR = "EUR", "EUR"
        UZS = "UZS", "UZS"

    title = models.CharField(_("name"), max_length=200)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=False)
    country = models.CharField(_("country"), max_length=120)
    city = models.CharField(_("city"), max_length=120, blank=True)
    description = models.TextField(_("short description"), max_length=500, blank=True)
    body = models.TextField(_("body"), help_text=_("Markdown is supported."))
    cover_image = models.ImageField(_("cover image"), upload_to="universities/")

    programs_offered = models.TextField(
        _("programs offered"),
        blank=True,
        help_text=_("Markdown list, e.g. '- Computer Science\\n- Economics'"),
    )
    tuition_from = models.DecimalField(
        _("tuition from (per year)"),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    currency = models.CharField(
        _("currency"),
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD,
    )
    world_ranking = models.PositiveIntegerField(_("world ranking"), null=True, blank=True)

    order = models.PositiveIntegerField(_("order"), default=0)
    is_active = models.BooleanField(_("active"), default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("university")
        verbose_name_plural = _("universities")
        ordering = ("order", "world_ranking", "title")

    def __str__(self):
        return self.title
