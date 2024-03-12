from django.urls import path
from .views import ActivityView

app_name = "activities"

urlpatterns = [
    path("", ActivityView.as_view(), name="activities"),
    path("<int:pk>/", ActivityView.as_view(), name="detail"),
    path("edit/<int:pk>/", ActivityView.as_view(), name="update"),
    path("delete/<int:pk>/", ActivityView.as_view(), name="delete"),
]
print("urlpatters", urlpatterns)