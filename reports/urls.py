from django.urls import path
from .views import ReportActivities, ReportHabits

app_name = "reports"

urlpatterns = [
    path(
        "most_performed_activity/",
        ReportActivities.as_view({"get": "get_most_performed_activity"}),
        name="most_performed_activity"
    ),
    path(
        "best_streak/",
        ReportActivities.as_view({"get": "get_best_streak"}),
        name="best_streak"
    ),
    path(
        "edges_difficulty_activities_to_perform/",
        ReportActivities.as_view({"get": "get_edges_difficulty_activities_to_perform"}),
        name="edges_difficulty_activities_to_perform"
    ),
    path(
        "habit_formation_progress/",
        ReportHabits.as_view({"get": "get_habit_formation_progress"}),
        name="habit_formation_progress"
    ),
    path(
        "habit_disintegration_progress/",
        ReportHabits.as_view({"get": "get_habit_disintegration_progress"}),
        name="habit_disintegration_progress"
    ),
]