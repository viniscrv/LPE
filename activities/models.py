from django.db import models

class Activity(models.Model):
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