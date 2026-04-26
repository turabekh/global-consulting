from django.contrib import admin

from .models import ContactInquiry, PartnershipInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "contact", "service_type", "status", "created_at")
    list_filter = ("status", "service_type", "created_at")
    search_fields = ("full_name", "contact", "note")
    list_editable = ("status",)
    readonly_fields = ("locale", "created_at")
    fieldsets = (
        (None, {"fields": ("full_name", "contact", "service_type", "note")}),
        ("Tracking", {"fields": ("status", "locale", "created_at")}),
    )


@admin.register(PartnershipInquiry)
class PartnershipInquiryAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("company_name", "contact", "goals")
    list_editable = ("status",)
    readonly_fields = ("locale", "created_at")
    fieldsets = (
        (None, {"fields": ("company_name", "contact", "goals")}),
        ("Tracking", {"fields": ("status", "locale", "created_at")}),
    )
