from django.urls import path

from .views import CurrentUserView
from .views_social import FacebookLogin, GoogleLogin

app_name = "users"

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="me"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/facebook/", FacebookLogin.as_view(), name="facebook_login"),
]
