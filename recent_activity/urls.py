from django.urls import path
from .views import RecentActivityView

app_name = "recent_activity"

urlpatterns = [
    path("", RecentActivityView.as_view(), name="recent_activity"),
]