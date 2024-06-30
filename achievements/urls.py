from django.urls import path
from .views import AchievementsView

app_name = "achievements"

urlpatterns = [
    path("achievements/", AchievementsView.as_view(), name="achievements"),
]