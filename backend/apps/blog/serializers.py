from rest_framework import serializers

from apps.core.markdown import render_markdown

from .models import BlogPost


class BlogPostListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    read_time_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            "id",
            "slug",
            "title",
            "excerpt",
            "category",
            "cover_image_url",
            "published_at",
            "read_time_minutes",
        )

    def get_cover_image_url(self, obj: BlogPost) -> str | None:
        if not obj.cover_image:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.cover_image.url
        return request.build_absolute_uri(obj.cover_image.url)


class BlogPostDetailSerializer(BlogPostListSerializer):
    body_html = serializers.SerializerMethodField()

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ("body", "body_html")

    def get_body_html(self, obj: BlogPost) -> str:
        return render_markdown(obj.body)
