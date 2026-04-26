from rest_framework import serializers

from .models import ContactInquiry, PartnershipInquiry


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ("full_name", "contact", "service_type", "note")

    def validate_full_name(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Full name is too short.")
        return value

    def validate_contact(self, value: str) -> str:
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError("Please enter a valid email or phone number.")
        return value


class PartnershipInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipInquiry
        fields = ("company_name", "contact", "goals")

    def validate_company_name(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Company name is too short.")
        return value

    def validate_contact(self, value: str) -> str:
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError("Please enter a valid email or phone number.")
        return value

    def validate_goals(self, value: str) -> str:
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError("Please describe your goals in more detail.")
        return value
