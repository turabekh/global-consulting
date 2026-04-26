from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactInquiry(models.Model):
    class ServiceType(models.TextChoices):
        TOURISM = "tourism", _("Tourism")
        STUDY = "study", _("Study")
        WORK = "work", _("Work")
        VISA = "visa", _("Visa Support")
        OTHER = "other", _("Other")

    class Status(models.TextChoices):
        NEW = "new", _("New")
        CONTACTED = "contacted", _("Contacted")
        CLOSED = "closed", _("Closed")

    full_name = models.CharField(_("full name"), max_length=120)
    contact = models.CharField(
        _("email or phone"),
        max_length=120,
        help_text=_("User-provided email address or phone number."),
    )
    service_type = models.CharField(
        _("service type"),
        max_length=16,
        choices=ServiceType.choices,
        default=ServiceType.OTHER,
    )
    note = models.TextField(_("note"), blank=True)

    status = models.CharField(
        _("status"),
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    locale = models.CharField(_("submitted in language"), max_length=8, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("contact inquiry")
        verbose_name_plural = _("contact inquiries")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.full_name} — {self.service_type}"


class PartnershipInquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", _("New")
        REVIEWING = "reviewing", _("Reviewing")
        ACCEPTED = "accepted", _("Accepted")
        DECLINED = "declined", _("Declined")
        CLOSED = "closed", _("Closed")

    company_name = models.CharField(_("company name"), max_length=200)
    contact = models.CharField(_("email or phone"), max_length=120)
    goals = models.TextField(_("goals and expectations"))

    status = models.CharField(
        _("status"),
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    locale = models.CharField(_("submitted in language"), max_length=8, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("partnership inquiry")
        verbose_name_plural = _("partnership inquiries")
        ordering = ("-created_at",)

    def __str__(self):
        return self.company_name
