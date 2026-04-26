from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Message

ONLINE_WINDOW_SECONDS = 60
EMAIL_THROTTLE_MINUTES = 10


def maybe_email_user(message: Message) -> None:
    if message.sender_role != Message.Sender.STAFF:
        return

    conversation = message.conversation
    user = conversation.application.user

    now = timezone.now()

    if user.last_ws_seen and (now - user.last_ws_seen) < timedelta(seconds=ONLINE_WINDOW_SECONDS):
        return

    if conversation.last_email_notification_at and (
        now - conversation.last_email_notification_at
    ) < timedelta(minutes=EMAIL_THROTTLE_MINUTES):
        return

    if not user.email:
        return

    application = conversation.application
    subject_label = application.target_label or application.get_service_type_display()
    subject = f"New message about your {subject_label} application"

    site_url = getattr(settings, "FRONTEND_URL", "http://localhost:9000")
    thread_url = f"{site_url}/#/dashboard/messages/{conversation.id}"

    context = {
        "user": user,
        "message": message,
        "application": application,
        "thread_url": thread_url,
        "subject_label": subject_label,
    }

    text_body = render_to_string("messaging/email/staff_reply.txt", context)
    html_body = render_to_string("messaging/email/staff_reply.html", context)

    send_mail(
        subject=subject,
        message=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_body,
        fail_silently=True,
    )

    conversation.last_email_notification_at = now
    conversation.save(update_fields=["last_email_notification_at", "updated_at"])
