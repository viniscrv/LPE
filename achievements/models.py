from django.db import models
from profiles.models import Profile
from activities.models import Activity

class Achievement(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    ACHIEVEMENT_TYPE_CHOICES = (
        ("new_habit", "new_habit"),
        ("new_easier_activity", "new_easier_activity"),
        ("new_harder_activity", "new_harder_activity"),
        ("new_best_streak", "new_best_streak"),
        ("new_more_performed", "new_more_performed"),
    )
    type = models.CharField(
        max_length=255, 
        choices=ACHIEVEMENT_TYPE_CHOICES, 
        blank=False, 
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)