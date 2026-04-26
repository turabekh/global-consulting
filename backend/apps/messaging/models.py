from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Conversation(models.Model):
    application = models.OneToOneField(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="conversation",
    )

    last_message_at = models.DateTimeField(
        _("last message at"), null=True, blank=True, db_index=True
    )
    last_user_read_at = models.DateTimeField(_("user last read"), null=True, blank=True)
    last_staff_read_at = models.DateTimeField(_("staff last read"), null=True, blank=True)
    last_email_notification_at = models.DateTimeField(
        _("last email notification at"),
        null=True,
        blank=True,
        help_text=_("Used to throttle email notifications."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("conversation")
        verbose_name_plural = _("conversations")
        ordering = ("-last_message_at", "-created_at")

    def __str__(self):
        return f"Conversation for {self.application.reference}"

    @property
    def user(self):
        return self.application.user


class Message(models.Model):
    class Sender(models.TextChoices):
        USER = "user", _("User")
        STAFF = "staff", _("Staff")
        SYSTEM = "system", _("System")

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
        help_text=_("User who sent the message. Null for system messages."),
    )
    sender_role = models.CharField(
        _("sender role"),
        max_length=8,
        choices=Sender.choices,
    )
    body = models.TextField(_("body"))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.sender_role}: {self.body[:60]}"
