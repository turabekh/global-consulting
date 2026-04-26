from django.db import models
from django.utils.translation import gettext_lazy as _


class FAQ(models.Model):
    class Category(models.TextChoices):
        GENERAL = "general", _("General")
        TOURISM = "tourism", _("Tourism")
        STUDY = "study", _("Study")
        WORK = "work", _("Work")
        VISA = "visa", _("Visa")

    category = models.CharField(
        _("category"),
        max_length=16,
        choices=Category.choices,
        default=Category.GENERAL,
        db_index=True,
    )
    question = models.CharField(_("question"), max_length=255)
    answer = models.TextField(_("answer"), help_text=_("Markdown is supported."))
    order = models.PositiveIntegerField(_("order"), default=0)
    is_active = models.BooleanField(_("active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ("category", "order", "id")

    def __str__(self):
        return self.question
