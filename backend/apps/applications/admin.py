from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Application, Document

SERVICE_ICONS = {
    "tourism": "🌴",
    "study": "🎓",
    "work": "💼",
    "visa": "📄",
}

STATUS_COLORS = {
    "draft": "#9ca3af",
    "submitted": "#4a8dff",
    "in_review": "#4a8dff",
    "needs_info": "#c97900",
    "accepted": "#1f9b62",
    "rejected": "#d04848",
    "closed": "#6b7280",
}


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ("kind", "file", "original_filename", "size_bytes", "verified_at", "uploaded_at")
    readonly_fields = ("original_filename", "size_bytes", "uploaded_at")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "service_emoji",
        "target_or_service",
        "user_email",
        "status_badge",
        "current_step",
        "submitted_at",
        "team_message_dot",
        "updated_at",
    )
    list_display_links = ("target_or_service",)
    list_filter = ("status", "service_type", "current_step")
    search_fields = (
        "reference",
        "target_label",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = (
        "reference",
        "user",
        "service_type",
        "target_slug",
        "target_label",
        "current_step",
        "data_summary",
        "conversation_link",
        "submitted_at",
        "decided_at",
        "created_at",
        "updated_at",
        "last_notified_status",
        "last_notified_team_message",
    )
    fieldsets = (
        (None, {"fields": ("reference", "user", "service_type", "target_label")}),
        ("Status", {"fields": ("status", "current_step", "submitted_at", "decided_at")}),
        ("Communication", {"fields": ("conversation_link", "team_message", "internal_notes")}),
        ("Application data", {"fields": ("data_summary",)}),
        ("Raw data (advanced)", {"classes": ("collapse",), "fields": ("data",)}),
        (
            "Internal tracking",
            {
                "classes": ("collapse",),
                "fields": (
                    "last_notified_status",
                    "last_notified_team_message",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    inlines = (DocumentInline,)
    ordering = ("-updated_at",)
    actions = (
        "mark_in_review",
        "mark_accepted",
        "mark_rejected",
        "mark_needs_info",
    )

    @admin.display(description="", ordering="service_type")
    def service_emoji(self, obj: Application) -> str:
        return SERVICE_ICONS.get(obj.service_type, "📋")

    @admin.display(description="Application", ordering="target_label")
    def target_or_service(self, obj: Application) -> str:
        return obj.target_label or obj.get_service_type_display()

    @admin.display(description="User", ordering="user__email")
    def user_email(self, obj: Application) -> str:
        return obj.user.email

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj: Application):
        color = STATUS_COLORS.get(obj.status, "#6b7280")
        return format_html(
            '<span style="display: inline-block; padding: 2px 10px; border-radius: 999px; '
            "background: {}22; color: {}; font-size: 11px; font-weight: 600; "
            'text-transform: uppercase; letter-spacing: 0.04em;">{}</span>',
            color,
            color,
            obj.get_status_display(),
        )

    @admin.display(description="Msg", boolean=False)
    def team_message_dot(self, obj: Application) -> str:
        if obj.team_message.strip():
            return "📝"
        return ""

    @admin.display(description="Application data")
    def data_summary(self, obj: Application):
        if not obj.data:
            return "(no data yet)"

        rows = []
        for key, value in obj.data.items():
            if value in (None, "", []):
                continue
            label = key.replace("_", " ").title()
            display = self._format_value(value)
            rows.append(
                format_html(
                    '<tr><td style="padding: 6px 12px 6px 0; color: #6b7280; '
                    "font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; "
                    'vertical-align: top; white-space: nowrap;">{}</td>'
                    '<td style="padding: 6px 0;">{}</td></tr>',
                    label,
                    display,
                )
            )

        if not rows:
            return "(no data yet)"

        table = format_html(
            '<table style="border-collapse: collapse;">{}</table>',
            mark_safe("".join(rows)),
        )
        return table

    @staticmethod
    def _format_value(value):
        if isinstance(value, bool):
            return "Yes" if value else "No"
        if isinstance(value, list | tuple):
            return ", ".join(str(v) for v in value)
        return str(value)

    @admin.action(description="Mark selected as In review")
    def mark_in_review(self, request, queryset):
        updated = queryset.exclude(status=Application.Status.IN_REVIEW).update(
            status=Application.Status.IN_REVIEW,
        )
        self.message_user(request, f"{updated} application(s) marked as In review.")

    @admin.action(description="Mark selected as Accepted")
    def mark_accepted(self, request, queryset):
        from django.utils import timezone

        for app in queryset.exclude(status=Application.Status.ACCEPTED):
            app.status = Application.Status.ACCEPTED
            app.decided_at = timezone.now()
            app.save()
        self.message_user(request, "Selected applications marked as Accepted.")

    @admin.action(description="Mark selected as Rejected")
    def mark_rejected(self, request, queryset):
        from django.utils import timezone

        for app in queryset.exclude(status=Application.Status.REJECTED):
            app.status = Application.Status.REJECTED
            app.decided_at = timezone.now()
            app.save()
        self.message_user(request, "Selected applications marked as Rejected.")

    @admin.action(description="Mark selected as Needs info")
    def mark_needs_info(self, request, queryset):
        updated = queryset.exclude(status=Application.Status.NEEDS_INFO).update(
            status=Application.Status.NEEDS_INFO,
        )
        self.message_user(request, f"{updated} application(s) marked as Needs info.")

    @admin.display(description="Conversation")
    def conversation_link(self, obj: Application):
        from django.urls import reverse

        try:
            conv = obj.conversation
        except Application.conversation.RelatedObjectDoesNotExist:
            return "(no conversation)"

        url = reverse("admin:messaging_conversation_change", args=[conv.pk])

        unread = ""
        if conv.last_message_at and (
            conv.last_staff_read_at is None or conv.last_message_at > conv.last_staff_read_at
        ):
            unread = mark_safe(
                '<span style="display: inline-block; margin-left: 8px; padding: 2px 8px; '
                "border-radius: 999px; background: #d04848; color: white; "
                'font-size: 11px; font-weight: 700;">unread</span>'
            )

        msg_count = conv.messages.count()
        last_msg = conv.messages.order_by("-created_at").first()
        preview = ""
        if last_msg:
            preview = format_html(
                '<div style="margin-top: 8px; padding: 10px 12px; background: #f3f0ff; '
                "border-left: 3px solid #6e5ef6; border-radius: 6px; font-size: 13px; "
                'color: #1a1a1a;"><strong>{}:</strong> {}</div>',
                last_msg.get_sender_role_display(),
                last_msg.body[:200] + ("…" if len(last_msg.body) > 200 else ""),
            )

        return format_html(
            '<a href="{}" style="color: #6e5ef6; font-weight: 600; '
            'text-decoration: none;">Open conversation ({} message{})</a>{}{}',
            url,
            msg_count,
            "" if msg_count == 1 else "s",
            unread,
            preview,
        )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "kind",
        "original_filename",
        "size_bytes",
        "verified_at",
        "uploaded_at",
    )
    list_filter = ("kind", "verified_at")
    search_fields = ("application__reference", "original_filename")
    readonly_fields = ("application", "original_filename", "size_bytes", "uploaded_at")
    ordering = ("-uploaded_at",)
