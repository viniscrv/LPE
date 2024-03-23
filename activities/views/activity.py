from django.shortcuts import get_object_or_404
from ..serializers import ActivitySerializer
from ..models import ActivityGroup, Activity
from profiles.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..mixins import ActivityMixin

class ActivityView(ActivityMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        profile = self.get_profile(request)

        if not pk:
            activities = Activity.objects.filter(profile=profile)
            serializer = ActivitySerializer(activities, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        activity = get_object_or_404(
            Activity.objects.filter(profile=profile), 
            pk=pk
        )

        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        profile = self.get_profile(request)

        data = request.data
        data.update({ "profile": profile.id })

        serializer = ActivitySerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        profile = self.get_profile(request)

        activity = get_object_or_404(Activity.objects.filter(profile=profile), pk=pk)
        serializer = ActivitySerializer(activity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        profile = self.get_profile(request)

        activity = get_object_or_404(Activity.objects.filter(profile=profile), pk=pk)
        activity.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ActivityByGroupView(ActivityMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        profile = self.get_profile(request)
        activity_group = get_object_or_404(ActivityGroup, pk=pk)

        activities = Activity.objects.filter(profile=profile, activity_group=activity_group)
        serializer = ActivitySerializer(activities, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)