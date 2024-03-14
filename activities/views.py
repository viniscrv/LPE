from django.shortcuts import render, get_object_or_404
from .serializers import ActivitySerializer, ReportActivitySerializer
from .models import Activity, ReportActivity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class ActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        if not pk:
            activities = Activity.objects.all()
            serializer = ActivitySerializer(activities, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data.update({ "profile": request.user.id })

        serializer = ActivitySerializer(data=data)

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
    
class ReportActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        if not pk:
            report_activities = ReportActivity.objects.all()
            serializer = ReportActivitySerializer(report_activities, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        report_activity = get_object_or_404(ReportActivity, pk=pk)
        serializer = ReportActivitySerializer(report_activity)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ReportActivitySerializer(data=request.data)

        if serializer.is_valid():

            report_already_done = ReportActivity.objects.filter(
                activity=request.data.get("activity"),
                created_at__contains=datetime.today().strftime("%Y-%m-%d")
            )

            if report_already_done:
                return Response({"detail": "Report has already been made for this activity today"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        report_activity = get_object_or_404(ReportActivity, pk=pk)
        serializer = ReportActivitySerializer(report_activity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        report_activity = get_object_or_404(ReportActivity, pk=pk)
        report_activity.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)