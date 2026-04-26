from rest_framework import serializers

from apps.core.markdown import render_markdown

from .models import TourPackage


class TourPackageListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    tag_list = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = TourPackage
        fields = (
            "id",
            "slug",
            "title",
            "destination",
            "description",
            "duration_days",
            "price_from",
            "currency",
            "tag_list",
            "cover_image_url",
        )

    def get_cover_image_url(self, obj: TourPackage) -> str | None:
        if not obj.cover_image:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.cover_image.url
        return request.build_absolute_uri(obj.cover_image.url)


class TourPackageDetailSerializer(TourPackageListSerializer):
    body_html = serializers.SerializerMethodField()

    class Meta(TourPackageListSerializer.Meta):
        fields = TourPackageListSerializer.Meta.fields + ("body", "body_html")

    def get_body_html(self, obj: TourPackage) -> str:
        return render_markdown(obj.body)
