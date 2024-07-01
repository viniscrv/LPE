from django.urls import path
from .views import RecentActivityView

app_name = "recent_activity"

urlpatterns = [
    path("recent_activity/", RecentActivityView.as_view(), name="recent_activity"),
]