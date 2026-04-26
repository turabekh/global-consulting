from rest_framework import serializers

from apps.core.markdown import render_markdown

from .models import University


class UniversityListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = (
            "id",
            "slug",
            "title",
            "country",
            "city",
            "description",
            "tuition_from",
            "currency",
            "world_ranking",
            "cover_image_url",
        )

    def get_cover_image_url(self, obj: University) -> str | None:
        if not obj.cover_image:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.cover_image.url
        return request.build_absolute_uri(obj.cover_image.url)


class UniversityDetailSerializer(UniversityListSerializer):
    body_html = serializers.SerializerMethodField()
    programs_offered_html = serializers.SerializerMethodField()

    class Meta(UniversityListSerializer.Meta):
        fields = UniversityListSerializer.Meta.fields + (
            "body",
            "body_html",
            "programs_offered",
            "programs_offered_html",
        )

    def get_body_html(self, obj: University) -> str:
        return render_markdown(obj.body)

    def get_programs_offered_html(self, obj: University) -> str:
        return render_markdown(obj.programs_offered)
