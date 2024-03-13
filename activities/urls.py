from django.urls import path
from .views import ActivityView, ReportActivityView

app_name = "activities"

urlpatterns = [
    path("", ActivityView.as_view(), name="activities"),
    path("<int:pk>/", ActivityView.as_view(), name="detail"),
    path("edit/<int:pk>/", ActivityView.as_view(), name="update"),
    path("delete/<int:pk>/", ActivityView.as_view(), name="delete"),
    path("report/", ReportActivityView.as_view(), name="report"),
    path("report/<int:pk>/", ReportActivityView.as_view(), name="report_detail"),
    path("report/edit/<int:pk>/", ReportActivityView.as_view(), name="report_update"),
    path("report/delete/<int:pk>/", ReportActivityView.as_view(), name="report_delete"),
]