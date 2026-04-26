from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Job(models.Model):
    class Currency(models.TextChoices):
        USD = "USD", "USD"
        EUR = "EUR", "EUR"
        UZS = "UZS", "UZS"

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", _("Full-time")
        PART_TIME = "part_time", _("Part-time")
        CONTRACT = "contract", _("Contract")
        INTERNSHIP = "internship", _("Internship")

    title = models.CharField(_("title"), max_length=200)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=False)
    country = models.CharField(_("country"), max_length=120)
    city = models.CharField(_("city"), max_length=120, blank=True)
    industry = models.CharField(_("industry"), max_length=120, blank=True)
    description = models.TextField(_("short description"), max_length=500, blank=True)
    body = models.TextField(_("body"), help_text=_("Markdown is supported."))
    cover_image = models.ImageField(_("cover image"), upload_to="jobs/")

    salary_from = models.DecimalField(
        _("salary from"),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    salary_to = models.DecimalField(
        _("salary to"),
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
    employment_type = models.CharField(
        _("employment type"),
        max_length=16,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
        db_index=True,
    )

    order = models.PositiveIntegerField(_("order"), default=0)
    is_active = models.BooleanField(_("active"), default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")
        ordering = ("order", "-created_at")

    def __str__(self):
        return self.title
