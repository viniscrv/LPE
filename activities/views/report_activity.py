from django.shortcuts import get_object_or_404
from ..serializers import ReportActivitySerializer, ActivitySerializer
from ..models import ReportActivity, Activity
from profiles.models import Profile
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework.decorators import action

class ReportActivityViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        profile = get_object_or_404(Profile, pk=request.user.id)

        if not pk:
            report_activities = ReportActivity.objects.filter(profile=profile)
            serializer = ReportActivitySerializer(report_activities, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        report_activity = get_object_or_404(ReportActivity, pk=pk)
        serializer = ReportActivitySerializer(report_activity)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        profile = get_object_or_404(Profile, pk=request.user.id)

        data = request.data
        data.update({ "profile": profile.pk })

        serializer = ReportActivitySerializer(data=request.data)

        if serializer.is_valid():

            report_already_done = ReportActivity.objects.filter(
                activity=request.data.get("activity"),
                profile=profile,
                created_at__contains=datetime.today().strftime("%Y-%m-%d")
            )

            if report_already_done:
                return Response({"detail": "Report has already been made for this activity today."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        profile = get_object_or_404(Profile, pk=request.user.id)

        report_activity = get_object_or_404(ReportActivity.objects.filter(profile=profile), pk=pk)
        serializer = ReportActivitySerializer(report_activity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        profile = get_object_or_404(Profile, pk=request.user.id)

        report_activity = get_object_or_404(ReportActivity.objects.filter(profile=profile), pk=pk)
        report_activity.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=["get"], detail=False)
    def get_pending_today(self, request):
        profile = get_object_or_404(Profile, pk=request.user.id)
        
        today_reports = ReportActivity.objects.filter(
            profile=profile,
            created_at__contains=datetime.today().strftime("%Y-%m-%d")
        )

        # TODO: lidar com recorrencia de atividades
        # TODO: lidar com until
        activities = Activity.objects.filter(
            profile=profile,
            recurrence="everyday"
        )

        reported_activities = [report.activity for report in today_reports]
        pending_activities = [
            activity for activity in activities 
            if activity not in reported_activities 
        ]

        serializer = ActivitySerializer(pending_activities, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
