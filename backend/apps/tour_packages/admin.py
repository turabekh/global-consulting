from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import TourPackage


@admin.register(TourPackage)
class TourPackageAdmin(TranslationAdmin):
    list_display = (
        "title",
        "destination",
        "duration_days",
        "price_from",
        "currency",
        "order",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "currency")
    search_fields = ("title", "destination", "description", "body", "tags")
    list_editable = ("order", "is_active")
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "destination", "cover_image")}),
        ("Content", {"fields": ("description", "body")}),
        ("Pricing & Duration", {"fields": ("duration_days", "price_from", "currency", "tags")}),
        ("Display", {"fields": ("order", "is_active")}),
        ("Timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
