from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone


def user_group(user_id: int) -> str:
    return f"user-{user_id}"


STAFF_GROUP = "staff-all"


class MessagesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user is None or isinstance(user, AnonymousUser):
            await self.close(code=4001)
            return

        self.user_id = user.id
        self.is_staff = user.is_staff

        await self.channel_layer.group_add(user_group(self.user_id), self.channel_name)
        if self.is_staff:
            await self.channel_layer.group_add(STAFF_GROUP, self.channel_name)

        await self.accept()
        await self.touch_seen(self.user_id)
        await self.send_json({"type": "connected"})

    async def disconnect(self, code):
        if hasattr(self, "user_id"):
            await self.channel_layer.group_discard(user_group(self.user_id), self.channel_name)
        if getattr(self, "is_staff", False):
            await self.channel_layer.group_discard(STAFF_GROUP, self.channel_name)

    async def receive_json(self, content, **kwargs):
        kind = content.get("type")
        if kind == "ping":
            await self.touch_seen(self.user_id)
            await self.send_json({"type": "pong"})

    async def message_created(self, event):
        await self.send_json(
            {
                "type": "message_created",
                "conversation_id": event["conversation_id"],
                "message": event["message"],
            }
        )

    @database_sync_to_async
    def touch_seen(self, user_id: int):
        from apps.users.models import User

        User.objects.filter(id=user_id).update(last_ws_seen=timezone.now())
