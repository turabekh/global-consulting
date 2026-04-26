from rest_framework import permissions, viewsets

from .models import University
from .serializers import UniversityDetailSerializer, UniversityListSerializer


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    lookup_field = "slug"

    def get_queryset(self):
        return University.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return UniversityListSerializer
        return UniversityDetailSerializer
