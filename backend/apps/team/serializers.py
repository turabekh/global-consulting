from rest_framework import serializers

from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ("id", "name", "role", "bio", "photo_url", "order")

    def get_photo_url(self, obj: TeamMember) -> str | None:
        if not obj.photo:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.photo.url
        return request.build_absolute_uri(obj.photo.url)
