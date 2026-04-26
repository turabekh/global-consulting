from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import VisaType


@admin.register(VisaType)
class VisaTypeAdmin(TranslationAdmin):
    list_display = (
        "title",
        "country",
        "category",
        "processing_time",
        "success_rate",
        "order",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "category", "country")
    search_fields = ("title", "country", "description", "body")
    list_editable = ("order", "is_active")
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "country", "category", "cover_image")}),
        ("Content", {"fields": ("description", "body")}),
        ("Stats", {"fields": ("processing_time", "success_rate")}),
        ("Display", {"fields": ("order", "is_active")}),
        ("Timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
