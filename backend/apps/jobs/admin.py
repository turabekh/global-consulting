from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Job


@admin.register(Job)
class JobAdmin(TranslationAdmin):
    list_display = (
        "title",
        "country",
        "city",
        "industry",
        "employment_type",
        "salary_from",
        "currency",
        "order",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "employment_type", "currency", "country")
    search_fields = ("title", "country", "city", "industry", "description", "body")
    list_editable = ("order", "is_active")
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "country", "city", "industry", "cover_image")}),
        ("Content", {"fields": ("description", "body")}),
        (
            "Salary & Type",
            {"fields": ("salary_from", "salary_to", "currency", "employment_type")},
        ),
        ("Display", {"fields": ("order", "is_active")}),
        ("Timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
