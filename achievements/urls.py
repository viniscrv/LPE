from django.urls import path
from .views import AchievementsView

app_name = "achievements"

urlpatterns = [
    path("", AchievementsView.as_view(), name="achievements"),
]