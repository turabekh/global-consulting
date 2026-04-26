from rest_framework import serializers

from apps.core.markdown import render_markdown

from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    body_html = serializers.SerializerMethodField()
    author_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = (
            "id",
            "author_name",
            "author_city",
            "author_photo_url",
            "body",
            "body_html",
            "order",
        )

    def get_body_html(self, obj: Testimonial) -> str:
        return render_markdown(obj.body)

    def get_author_photo_url(self, obj: Testimonial) -> str | None:
        if not obj.author_photo:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.author_photo.url
        return request.build_absolute_uri(obj.author_photo.url)
