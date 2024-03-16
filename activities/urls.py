from django.urls import path
from .views import ActivityGroupView, ActivityView, ReportActivityView

app_name = "activities"

urlpatterns = [
    path("", ActivityView.as_view(), name="activities"),
    path("<int:pk>/", ActivityView.as_view(), name="detail"),
    path("edit/<int:pk>/", ActivityView.as_view(), name="update"),
    path("delete/<int:pk>/", ActivityView.as_view(), name="delete"),
    path("groups/", ActivityGroupView.as_view(), name="groups"),
    path("groups/<int:pk>/", ActivityGroupView.as_view(), name="group_detail"),
    path("groups/edit/<int:pk>/", ActivityGroupView.as_view(), name="group_update"),
    path("groups/delete/<int:pk>/", ActivityGroupView.as_view(), name="group_delete"),
    path("report/", ReportActivityView.as_view(), name="report"),
    path("report/<int:pk>/", ReportActivityView.as_view(), name="report_detail"),
    path("report/edit/<int:pk>/", ReportActivityView.as_view(), name="report_update"),
    path("report/delete/<int:pk>/", ReportActivityView.as_view(), name="report_delete"),
]