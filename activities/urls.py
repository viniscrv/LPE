from django.urls import path
from .views import ActivityGroupView, ActivityView, ReportActivityViewSet, ActivityByGroupView

app_name = "activities"

urlpatterns = [
    path("", ActivityView.as_view(), name="activities"),
    path("<int:pk>/", ActivityView.as_view(), name="detail"),
    path("edit/<int:pk>/", ActivityView.as_view(), name="update"),
    path("delete/<int:pk>/", ActivityView.as_view(), name="delete"),
    path("by_group/<int:pk>/", ActivityByGroupView.as_view(), name="by_group"),
    path("groups/", ActivityGroupView.as_view(), name="groups"),
    path("groups/<int:pk>/", ActivityGroupView.as_view(), name="group_detail"),
    path("groups/edit/<int:pk>/", ActivityGroupView.as_view(), name="group_update"),
    path("groups/delete/<int:pk>/", ActivityGroupView.as_view(), name="group_delete"),
    path("report/", ReportActivityViewSet.as_view({"get": "get", "post": "post"}), name="report"),
    path("report/<int:pk>/", ReportActivityViewSet.as_view({"get": "get"}), name="report_detail"),
    path("report/edit/<int:pk>/", ReportActivityViewSet.as_view({"patch": "patch"}), name="report_update"),
    path("report/delete/<int:pk>/", ReportActivityViewSet.as_view({"delete": "delete"}), name="report_delete"),
    path("report/pending_today/", ReportActivityViewSet.as_view({"get": "get_pending_today"}), name="report_pending_today"),
    path("report/history_today/", ReportActivityViewSet.as_view({"get": "get_report_history_today"}), name="report_history_today"),
    path("report/history/", ReportActivityViewSet.as_view({"get": "get_report_history"}), name="report_history"),
]