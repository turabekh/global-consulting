from rest_framework import serializers

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "sender_role", "author", "body", "created_at")
        read_only_fields = ("id", "sender_role", "author", "created_at")


class ConversationListSerializer(serializers.ModelSerializer):
    application_reference = serializers.UUIDField(source="application.reference", read_only=True)
    application_target_label = serializers.CharField(
        source="application.target_label", read_only=True
    )
    application_service_type = serializers.CharField(
        source="application.service_type", read_only=True
    )
    application_status = serializers.CharField(source="application.status", read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "id",
            "application_reference",
            "application_target_label",
            "application_service_type",
            "application_status",
            "last_message_at",
            "last_message",
            "unread_count",
        )

    def get_last_message(self, obj: Conversation):
        message = obj.messages.order_by("-created_at").first()
        if not message:
            return None
        return {
            "id": message.id,
            "sender_role": message.sender_role,
            "body": message.body[:160],
            "created_at": message.created_at,
        }

    def get_unread_count(self, obj: Conversation) -> int:
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return 0

        is_staff = request.user.is_staff
        from_role = "staff" if not is_staff else "user"
        last_read = obj.last_staff_read_at if is_staff else obj.last_user_read_at

        qs = obj.messages.filter(sender_role=from_role)
        if last_read:
            qs = qs.filter(created_at__gt=last_read)
        return qs.count()


class ConversationDetailSerializer(ConversationListSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ConversationListSerializer.Meta):
        fields = ConversationListSerializer.Meta.fields + ("messages",)


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("body",)

    def validate_body(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Message cannot be empty.")
        if len(value) > 5000:
            raise serializers.ValidationError("Message is too long (max 5000 characters).")
        return value
