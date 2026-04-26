from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.applications.models import Application

from .consumers import STAFF_GROUP, user_group
from .models import Conversation, Message
from .notifications import maybe_email_user


@receiver(post_save, sender=Application)
def ensure_conversation_for_application(sender, instance: Application, created: bool, **kwargs):
    if created:
        Conversation.objects.get_or_create(application=instance)


@receiver(post_save, sender=Message)
def broadcast_new_message(sender, instance: Message, created: bool, **kwargs):
    if not created:
        return

    layer = get_channel_layer()
    if layer is None:
        return

    payload = {
        "id": instance.id,
        "sender_role": instance.sender_role,
        "author": instance.author_id,
        "body": instance.body,
        "created_at": instance.created_at.isoformat(),
    }

    user_id = instance.conversation.application.user_id

    async_to_sync(layer.group_send)(
        user_group(user_id),
        {
            "type": "message_created",
            "conversation_id": instance.conversation_id,
            "message": payload,
        },
    )

    async_to_sync(layer.group_send)(
        STAFF_GROUP,
        {
            "type": "message_created",
            "conversation_id": instance.conversation_id,
            "message": payload,
        },
    )

    maybe_email_user(instance)
