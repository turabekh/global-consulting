from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        path = f"/api/auth/registration/account-confirm-email/{emailconfirmation.key}/"
        if request:
            return request.build_absolute_uri(path)
        backend_url = getattr(settings, "BACKEND_URL", "http://localhost:8000")
        return f"{backend_url}{path}"

    def format_email_subject(self, subject):
        return subject
