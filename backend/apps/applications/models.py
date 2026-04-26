import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Application(models.Model):
    class ServiceType(models.TextChoices):
        TOURISM = "tourism", _("Tourism")
        STUDY = "study", _("Study")
        WORK = "work", _("Work")
        VISA = "visa", _("Visa")

    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SUBMITTED = "submitted", _("Submitted")
        IN_REVIEW = "in_review", _("In Review")
        NEEDS_INFO = "needs_info", _("Needs Info")
        ACCEPTED = "accepted", _("Accepted")
        REJECTED = "rejected", _("Rejected")
        CLOSED = "closed", _("Closed")

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    service_type = models.CharField(
        _("service type"),
        max_length=16,
        choices=ServiceType.choices,
        db_index=True,
    )

    target_slug = models.CharField(
        _("target item slug"),
        max_length=255,
        blank=True,
        help_text=_("Slug of the target catalog item (e.g. 'mit', 'bali-cultural-adventure')."),
    )

    target_label = models.CharField(
        _("target item label"),
        max_length=255,
        blank=True,
        help_text=_("Human-readable label cached at submission time."),
    )

    status = models.CharField(
        _("status"),
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    current_step = models.PositiveSmallIntegerField(
        _("current step"),
        default=1,
        help_text=_("Highest step the user has reached in the multi-step form."),
    )

    data = models.JSONField(
        _("application data"),
        default=dict,
        blank=True,
        help_text=_("Per-service form fields. Schema varies by service_type."),
    )

    internal_notes = models.TextField(
        _("internal notes"),
        blank=True,
        help_text=_("Notes from staff. Not shown to the user."),
    )

    submitted_at = models.DateTimeField(_("submitted at"), null=True, blank=True)
    decided_at = models.DateTimeField(_("decided at"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("application")
        verbose_name_plural = _("applications")
        ordering = ("-updated_at",)

    def __str__(self):
        return f"{self.user.email} — {self.get_service_type_display()} ({self.status})"


def document_upload_path(instance: "Document", filename: str) -> str:
    return f"applications/{instance.application.reference}/{filename}"


class Document(models.Model):
    class Kind(models.TextChoices):
        PASSPORT = "passport", _("Passport")
        TRANSCRIPT = "transcript", _("Transcript")
        CV = "cv", _("CV / Resume")
        FINANCIAL = "financial", _("Financial statement")
        CERTIFICATE = "certificate", _("Certificate")
        PHOTO = "photo", _("Photo")
        OTHER = "other", _("Other")

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    kind = models.CharField(
        _("kind"),
        max_length=16,
        choices=Kind.choices,
        default=Kind.OTHER,
    )

    file = models.FileField(_("file"), upload_to=document_upload_path)
    original_filename = models.CharField(_("original filename"), max_length=255, blank=True)
    size_bytes = models.PositiveBigIntegerField(_("size (bytes)"), default=0)

    verified_at = models.DateTimeField(_("verified at"), null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_documents",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ("-uploaded_at",)

    def __str__(self):
        return f"{self.application.reference} — {self.kind} — {self.original_filename}"
