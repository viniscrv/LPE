from django.db import models
from profiles.models import Profile
from activities.models import Activity

class RecentActivity(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    RECENT_ACTIVITY_TYPE_CHOICES = (
        ("complete_report", "complete_report"),
        ("delete_report", "delete_report"),
        ("edit_report", "edit_report"),
    )
    type = models.CharField(
        max_length=255, 
        choices=RECENT_ACTIVITY_TYPE_CHOICES, 
        blank=False, 
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)