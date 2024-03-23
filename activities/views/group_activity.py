from django.shortcuts import get_object_or_404
from ..serializers import ActivityGroupSerializer
from ..models import ActivityGroup
from profiles.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..mixins import ActivityMixin

class ActivityGroupView(ActivityMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        profile = self.get_profile(request)

        if not pk:
            activity_groups = ActivityGroup.objects.filter(profile=profile)
            serializer = ActivityGroupSerializer(activity_groups, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        activity_group = get_object_or_404(
            ActivityGroup.objects.filter(profile=profile), 
            pk=pk
        )

        serializer = ActivityGroupSerializer(activity_group)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        profile = self.get_profile(request)

        data = request.data
        data.update({ "profile": profile.id })

        serializer = ActivityGroupSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        profile = self.get_profile(request)

        activity_group = get_object_or_404(ActivityGroup.objects.filter(profile=profile), pk=pk)
        serializer = ActivityGroupSerializer(activity_group, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        profile = self.get_profile(request)

        activity_group = get_object_or_404(ActivityGroup.objects.filter(profile=profile), pk=pk)
        activity_group.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)