from rest_framework import serializers

from .models import Application, Document


class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = (
            "id",
            "kind",
            "file",
            "file_url",
            "original_filename",
            "size_bytes",
            "is_verified",
            "uploaded_at",
        )
        extra_kwargs = {
            "file": {"write_only": True},
            "size_bytes": {"read_only": True},
            "original_filename": {"read_only": True},
        }

    def get_file_url(self, obj: Document) -> str | None:
        if not obj.file:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.file.url
        return request.build_absolute_uri(obj.file.url)

    def get_is_verified(self, obj: Document) -> bool:
        return obj.verified_at is not None


class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "reference",
            "service_type",
            "target_slug",
            "target_label",
            "status",
            "current_step",
            "submitted_at",
            "decided_at",
            "created_at",
            "updated_at",
        )


class ApplicationDetailSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = (
            "reference",
            "service_type",
            "target_slug",
            "target_label",
            "status",
            "current_step",
            "data",
            "documents",
            "team_message",
            "submitted_at",
            "decided_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "reference",
            "status",
            "team_message",
            "submitted_at",
            "decided_at",
            "created_at",
            "updated_at",
        )

    def validate_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("data must be an object.")
        return value


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "service_type",
            "target_slug",
            "target_label",
            "data",
        )

    def validate_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("data must be an object.")
        return value
