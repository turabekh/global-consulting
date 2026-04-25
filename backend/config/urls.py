from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


def password_reset_placeholder(request, uidb64, token):
    return HttpResponse(
        f"<h1>Password reset link</h1>"
        f"<p>UID: {uidb64}</p><p>Token: {token}</p>"
        f"<p>Placeholder. Frontend will replace this.</p>"
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "password-reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_placeholder,
        name="password_reset_confirm",
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]


admin.site.site_header = "Global Consulting Admin"
admin.site.site_title = "Global Consulting"
admin.site.index_title = "Administration"
