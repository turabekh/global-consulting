from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _


class TourPackage(models.Model):
    class Currency(models.TextChoices):
        USD = "USD", "USD"
        EUR = "EUR", "EUR"
        UZS = "UZS", "UZS"

    title = models.CharField(_("title"), max_length=200)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=False)
    destination = models.CharField(_("destination"), max_length=200)
    description = models.TextField(_("short description"), max_length=500, blank=True)
    body = models.TextField(_("body"), help_text=_("Markdown is supported."))
    cover_image = models.ImageField(_("cover image"), upload_to="tour-packages/")

    duration_days = models.PositiveIntegerField(_("duration in days"), default=0)
    price_from = models.DecimalField(
        _("price from"),
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
    tags = models.CharField(
        _("tags"),
        max_length=200,
        blank=True,
        help_text=_("Comma-separated, e.g. beach,culture,adventure"),
    )

    order = models.PositiveIntegerField(_("order"), default=0)
    is_active = models.BooleanField(_("active"), default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("tour package")
        verbose_name_plural = _("tour packages")
        ordering = ("order", "-created_at")

    def __str__(self):
        return self.title

    @property
    def tag_list(self) -> list[str]:
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]
