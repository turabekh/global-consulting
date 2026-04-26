from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    list_display = ("author_name", "author_city", "order", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("author_name", "author_city", "body")
    list_editable = ("order", "is_active")
    ordering = ("order", "id")
