from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ("question", "category", "order", "is_active", "updated_at")
    list_filter = ("category", "is_active")
    search_fields = ("question", "answer")
    list_editable = ("category", "order", "is_active")
    ordering = ("category", "order", "id")
