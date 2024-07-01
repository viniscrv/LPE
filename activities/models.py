from django.db import models
from datetime import datetime
from profiles.models import Profile

from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
# from recent_activity.utils import create_recent_activity

class ActivityGroup(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_group = models.ForeignKey(ActivityGroup, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    RECURRENCE_CHOICES = (
        ("everyday", "everyday"),
        ("weekend", "weekend"),
        ("week", "week")
    )
    recurrence = models.CharField(
        max_length=255, 
        choices=RECURRENCE_CHOICES, 
        blank=False, 
        null=False
    )
    until = models.DateField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # TODO: period

    def __str__(self):
        return self.name

class ReportActivity(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    EFFORT_PERCEPTION_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
    )
    effort_perception = models.CharField(
        max_length=255, 
        choices=EFFORT_PERCEPTION_CHOICES, 
        blank=False, 
        null=False
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.completed is True:
            self.completed_at = datetime.now()
        else:
            self.completed_at = None

        return super().save(*args, **kwargs)
    

@receiver(signal=post_save, sender=ReportActivity)
def create(sender, instance, **kwargs):
    from recent_activity.utils import create_recent_activity

    create_recent_activity(
        profile=instance.profile,
        activity=instance.activity,
        type="create",
    )