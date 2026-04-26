from django.utils import translation
from rest_framework import generics, permissions

from .models import ContactInquiry, PartnershipInquiry
from .serializers import ContactInquirySerializer, PartnershipInquirySerializer


class ContactInquiryCreateView(generics.CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(locale=translation.get_language() or "")


class PartnershipInquiryCreateView(generics.CreateAPIView):
    queryset = PartnershipInquiry.objects.all()
    serializer_class = PartnershipInquirySerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(locale=translation.get_language() or "")
