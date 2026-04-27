from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Application

NOTIFIABLE_STATUSES = {
    Application.Status.IN_REVIEW,
    Application.Status.NEEDS_INFO,
    Application.Status.ACCEPTED,
    Application.Status.REJECTED,
    Application.Status.CLOSED,
}


@receiver(post_save, sender=Application)
def notify_application_update(sender, instance: Application, created: bool, **kwargs):
    if created:
        return

    notify_status = (
        instance.status in NOTIFIABLE_STATUSES and instance.status != instance.last_notified_status
    )
    notify_message = (
        bool(instance.team_message.strip())
        and instance.team_message != instance.last_notified_team_message
    )

    if not (notify_status or notify_message):
        return

    user = instance.user
    if not user.email:
        return

    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:9000")
    detail_url = f"{frontend_url}/#/dashboard/applications/{instance.reference}"

    subject_label = instance.target_label or instance.get_service_type_display()
    status_label = instance.get_status_display()

    context = {
        "user": user,
        "application": instance,
        "subject_label": subject_label,
        "status_label": status_label,
        "team_message": instance.team_message,
        "detail_url": detail_url,
        "notify_status": notify_status,
        "notify_message": notify_message,
    }

    subject = render_to_string("email/application_update_subject.txt", context).strip()
    text_body = render_to_string("email/application_update.txt", context)
    html_body = render_to_string("email/application_update.html", context)

    send_mail(
        subject=subject,
        message=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_body,
        fail_silently=True,
    )

    Application.objects.filter(pk=instance.pk).update(
        last_notified_status=instance.status,
        last_notified_team_message=instance.team_message,
    )
