from django.contrib import admin
from django.utils import timezone

from .models import Application, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ("kind", "file", "original_filename", "size_bytes", "uploaded_at", "verified_at")
    readonly_fields = ("file", "original_filename", "size_bytes", "uploaded_at")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "reference_short",
        "user",
        "service_type",
        "target_label",
        "status",
        "current_step",
        "submitted_at",
        "updated_at",
    )
    list_filter = ("status", "service_type", "submitted_at", "created_at")
    search_fields = (
        "reference",
        "target_label",
        "target_slug",
        "user__email",
        "user__first_name",
        "user__last_name",
        "internal_notes",
    )
    list_editable = ("status",)
    readonly_fields = (
        "reference",
        "data",
        "current_step",
        "submitted_at",
        "decided_at",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = ("user",)
    inlines = (DocumentInline,)
    fieldsets = (
        (None, {"fields": ("reference", "user", "service_type", "target_slug", "target_label")}),
        ("Status", {"fields": ("status", "current_step", "submitted_at", "decided_at")}),
        ("Internal", {"fields": ("internal_notes",)}),
        ("Data (read-only)", {"classes": ("collapse",), "fields": ("data",)}),
        ("Timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Reference", ordering="reference")
    def reference_short(self, obj: Application) -> str:
        return str(obj.reference)[:8]

    def save_model(self, request, obj: Application, form, change):
        if (
            change
            and "status" in form.changed_data
            and obj.status in ("accepted", "rejected", "closed")
            and obj.decided_at is None
        ):
            obj.decided_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "kind",
        "original_filename",
        "size_bytes",
        "uploaded_at",
        "verified_at",
    )
    list_filter = ("kind", "verified_at", "uploaded_at")
    search_fields = (
        "application__reference",
        "application__user__email",
        "original_filename",
    )
    readonly_fields = (
        "application",
        "file",
        "original_filename",
        "size_bytes",
        "uploaded_at",
    )
    autocomplete_fields = ("verified_by",)
