from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin):
    list_display = (
        "title",
        "category",
        "is_published",
        "published_at",
        "author",
        "updated_at",
    )
    list_filter = ("category", "is_published", "published_at")
    search_fields = ("title", "excerpt", "body")
    list_editable = ("category", "is_published")
    autocomplete_fields = ("author",)
    readonly_fields = ("slug", "published_at", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "cover_image")}),
        ("Content", {"fields": ("excerpt", "body")}),
        ("Publishing", {"fields": ("author", "is_published", "published_at")}),
        ("Timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
