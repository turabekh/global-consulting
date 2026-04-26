from rest_framework import serializers

from apps.core.markdown import render_markdown

from .models import VisaType


class VisaTypeListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = VisaType
        fields = (
            "id",
            "slug",
            "title",
            "country",
            "category",
            "description",
            "processing_time",
            "success_rate",
            "cover_image_url",
        )

    def get_cover_image_url(self, obj: VisaType) -> str | None:
        if not obj.cover_image:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.cover_image.url
        return request.build_absolute_uri(obj.cover_image.url)


class VisaTypeDetailSerializer(VisaTypeListSerializer):
    body_html = serializers.SerializerMethodField()

    class Meta(VisaTypeListSerializer.Meta):
        fields = VisaTypeListSerializer.Meta.fields + ("body", "body_html")

    def get_body_html(self, obj: VisaType) -> str:
        return render_markdown(obj.body)
