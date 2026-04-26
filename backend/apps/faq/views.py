from rest_framework import permissions, viewsets

from .models import FAQ
from .serializers import FAQSerializer


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FAQSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filterset_fields = ("category",)

    def get_queryset(self):
        qs = FAQ.objects.filter(is_active=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs
