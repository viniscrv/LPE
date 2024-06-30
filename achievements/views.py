from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Achievement
from .serializers import AchievementSerializer
from django.shortcuts import get_object_or_404
from profiles.models import Profile

class AchievementsView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_profile(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        return profile

    def get(self, request):
        profile = self._get_profile(request)

        achievements = Achievement.objects.filter(profile=profile)

        if achievements:
            achievements = achievements[-8:]

        serializer = AchievementSerializer(achievements, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)