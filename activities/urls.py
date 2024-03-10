from django.urls import path
from .views import ActivityView

app_name = "activities"

urlpatterns = [
    path("", ActivityView.as_view(), name="activities")
]
print("urlpatters", urlpatterns)