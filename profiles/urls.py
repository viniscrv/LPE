from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ProfileView

app_name = "profiles"

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileView.as_view(), name='me'),
    path('register/', ProfileView.as_view(), name='register'),
    path('profile/edit/', ProfileView.as_view(), name='edit'),
]