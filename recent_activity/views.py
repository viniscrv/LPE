from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import RecentActivity
from .serializers import RecentActivitySerializer
from django.shortcuts import get_object_or_404
from profiles.models import Profile

class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_profile(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        return profile

    def get(self, request):
        profile = self._get_profile(request)

        recent_activities = RecentActivity.objects.filter(profile=profile)

        if recent_activities:
            recent_activities = recent_activities[-8:]

        serializer = RecentActivitySerializer(recent_activities, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)