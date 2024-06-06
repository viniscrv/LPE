from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ProfileView

app_name = "profiles"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ProfileView.as_view({"get": "get"}), name="me"),
    path("register/", ProfileView.as_view({"post": "post"}), name="register"),
    path("profile/edit/", ProfileView.as_view({"patch": "patch"}), name="edit"),
    path("profile/edit_password/", ProfileView.as_view({"patch": "edit_password"}), name="edit_password"),
]
