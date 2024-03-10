from django.shortcuts import render
from .serializers import ActivitySerializer
from .models import Activity
from rest_framework.views import APIView
from rest_framework.response import Response

class ActivityView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)

        return Response(serializer.data)