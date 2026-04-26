from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ("sender_role", "author", "body", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("author",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "user_email",
        "last_message_at",
        "unread_for_staff",
        "updated_at",
    )
    list_filter = ("last_message_at",)
    search_fields = (
        "application__reference",
        "application__user__email",
        "application__target_label",
    )
    readonly_fields = (
        "application",
        "last_message_at",
        "last_user_read_at",
        "last_staff_read_at",
        "last_email_notification_at",
        "created_at",
        "updated_at",
    )
    inlines = (MessageInline,)

    @admin.display(description="User", ordering="application__user__email")
    def user_email(self, obj: Conversation) -> str:
        return obj.application.user.email

    @admin.display(description="Unread for staff", boolean=True)
    def unread_for_staff(self, obj: Conversation) -> bool:
        if obj.last_message_at is None:
            return False
        if obj.last_staff_read_at is None:
            return True
        return obj.last_message_at > obj.last_staff_read_at


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender_role", "author", "short_body", "created_at")
    list_filter = ("sender_role", "created_at")
    search_fields = ("body", "conversation__application__reference")
    autocomplete_fields = ("author",)
    readonly_fields = ("created_at",)

    @admin.display(description="Body")
    def short_body(self, obj: Message) -> str:
        return obj.body[:80] + ("…" if len(obj.body) > 80 else "")
