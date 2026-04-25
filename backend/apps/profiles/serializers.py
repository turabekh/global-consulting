from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "language",
            "timezone",
            "bio",
            "avatar",
            "avatar_url",
        )
        extra_kwargs = {
            "avatar": {"write_only": True, "required": False},
        }

    def get_avatar_url(self, obj: Profile) -> str | None:
        if not obj.avatar:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.avatar.url
        return request.build_absolute_uri(obj.avatar.url)
