from rest_framework import serializers

from apps.core.markdown import render_markdown

from .models import Job


class JobListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            "id",
            "slug",
            "title",
            "country",
            "city",
            "industry",
            "description",
            "salary_from",
            "salary_to",
            "currency",
            "employment_type",
            "cover_image_url",
        )

    def get_cover_image_url(self, obj: Job) -> str | None:
        if not obj.cover_image:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.cover_image.url
        return request.build_absolute_uri(obj.cover_image.url)


class JobDetailSerializer(JobListSerializer):
    body_html = serializers.SerializerMethodField()

    class Meta(JobListSerializer.Meta):
        fields = JobListSerializer.Meta.fields + ("body", "body_html")

    def get_body_html(self, obj: Job) -> str:
        return render_markdown(obj.body)
