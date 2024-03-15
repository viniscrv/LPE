from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(default="", blank=True)

    def __str__(self):
        return self.profile.get_username()