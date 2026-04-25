from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
    list_display = ("name", "role", "order", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "role")
    list_editable = ("order", "is_active")
    ordering = ("order", "id")
