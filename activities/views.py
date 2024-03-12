from django.shortcuts import render, get_object_or_404
from .serializers import ActivitySerializer
from .models import Activity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ActivityView(APIView):
    def get(self, request, pk=None):

        if not pk:
            activities = Activity.objects.all()
            serializer = ActivitySerializer(activities, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(activity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        activity.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)