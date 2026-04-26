from rest_framework import permissions, viewsets

from .models import VisaType
from .serializers import VisaTypeDetailSerializer, VisaTypeListSerializer


class VisaTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    lookup_field = "slug"

    def get_queryset(self):
        qs = VisaType.objects.filter(is_active=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return VisaTypeListSerializer
        return VisaTypeDetailSerializer
