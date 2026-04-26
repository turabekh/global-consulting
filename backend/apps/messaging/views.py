from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageCreateSerializer,
    MessageSerializer,
)


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Conversation.objects.all().select_related("application", "application__user")
        return Conversation.objects.filter(application__user=user).select_related("application")

    def get_serializer_class(self):
        if self.action == "list":
            return ConversationListSerializer
        return ConversationDetailSerializer

    @action(detail=True, methods=["post"], url_path="messages")
    def post_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender_role = "staff" if request.user.is_staff else "user"
        message = Message.objects.create(
            conversation=conversation,
            author=request.user,
            sender_role=sender_role,
            body=serializer.validated_data["body"],
        )

        now = timezone.now()
        conversation.last_message_at = now
        if sender_role == "user":
            conversation.last_user_read_at = now
        else:
            conversation.last_staff_read_at = now
        conversation.save(
            update_fields=[
                "last_message_at",
                "last_user_read_at",
                "last_staff_read_at",
                "updated_at",
            ]
        )

        out = MessageSerializer(message)
        return Response(out.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        conversation = self.get_object()
        now = timezone.now()
        if request.user.is_staff:
            conversation.last_staff_read_at = now
            conversation.save(update_fields=["last_staff_read_at", "updated_at"])
        else:
            conversation.last_user_read_at = now
            conversation.save(update_fields=["last_user_read_at", "updated_at"])
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
