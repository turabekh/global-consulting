from rest_framework import permissions, viewsets

from .models import Job
from .serializers import JobDetailSerializer, JobListSerializer


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    lookup_field = "slug"

    def get_queryset(self):
        qs = Job.objects.filter(is_active=True)
        employment_type = self.request.query_params.get("employment_type")
        if employment_type:
            qs = qs.filter(employment_type=employment_type)
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return JobListSerializer
        return JobDetailSerializer
