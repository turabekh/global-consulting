from rest_framework import permissions, viewsets

from .models import TourPackage
from .serializers import TourPackageDetailSerializer, TourPackageListSerializer


class TourPackageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    lookup_field = "slug"

    def get_queryset(self):
        return TourPackage.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return TourPackageListSerializer
        return TourPackageDetailSerializer
