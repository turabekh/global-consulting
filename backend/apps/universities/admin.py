from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import University


@admin.register(University)
class UniversityAdmin(TranslationAdmin):
    list_display = (
        "title",
        "country",
        "city",
        "tuition_from",
        "currency",
        "world_ranking",
        "order",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "currency", "country")
    search_fields = ("title", "country", "city", "description", "body")
    list_editable = ("order", "is_active")
    readonly_fields = ("slug", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "country", "city", "cover_image")}),
        ("Content", {"fields": ("description", "body", "programs_offered")}),
        ("Tuition & Ranking", {"fields": ("tuition_from", "currency", "world_ranking")}),
        ("Display", {"fields": ("order", "is_active")}),
        ("Timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
