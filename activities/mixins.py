from abc import ABC
from profiles.models import Profile
from django.shortcuts import get_object_or_404

class ActivityMixin(ABC):
    def get_profile(self, request):
        profile = get_object_or_404(Profile, pk=request.user.id)

        return profile