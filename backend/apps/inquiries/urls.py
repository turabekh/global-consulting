from django.urls import path

from .views import ContactInquiryCreateView, PartnershipInquiryCreateView

app_name = "inquiries"

urlpatterns = [
    path("contact/", ContactInquiryCreateView.as_view(), name="contact"),
    path("partnership/", PartnershipInquiryCreateView.as_view(), name="partnership"),
]
