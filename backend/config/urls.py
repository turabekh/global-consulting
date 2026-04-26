from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

admin.site.site_header = "Global Consulting Admin"
admin.site.site_title = "Global Consulting"
admin.site.index_title = "Administration"


def password_reset_redirect(request, uidb64, token):
    frontend = "http://localhost:9000"
    return HttpResponseRedirect(f"{frontend}/#/reset-password/{uidb64}/{token}")


def email_confirm_redirect(request, key):
    frontend = "http://localhost:9000"
    return HttpResponseRedirect(f"{frontend}/#/verify-email/{key}")


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/auth/registration/account-confirm-email/<str:key>/",
        email_confirm_redirect,
        name="account_confirm_email",
    ),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/users/", include("apps.users.urls")),
    path("api/team/", include("apps.team.urls")),
    path("api/testimonials/", include("apps.testimonials.urls")),
    path("api/inquiries/", include("apps.inquiries.urls")),
    path("api/faq/", include("apps.faq.urls")),
    path("api/blog/", include("apps.blog.urls")),
    path("accounts/", include("allauth.urls")),
    path(
        "password-reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_redirect,
        name="password_reset_confirm",
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
