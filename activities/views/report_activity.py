from django.shortcuts import get_object_or_404
from ..serializers import ReportActivitySerializer, ActivitySerializer
from ..models import ReportActivity, Activity
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
from rest_framework.decorators import action
from ..mixins import ActivityMixin

class ReportActivityViewSet(ActivityMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        profile = self.get_profile(request)

        if not pk:
            report_activities = ReportActivity.objects.filter(profile=profile)

            paginator = PageNumberPagination()
            # paginator.page_size = 10
            page = paginator.paginate_queryset(report_activities, request)
            
            serializer = ReportActivitySerializer(page, many=True)

            return paginator.get_paginated_response(serializer.data)

        report_activity = get_object_or_404(
            ReportActivity.objects.filter(profile=profile), 
            pk=pk
        )
        
        serializer = ReportActivitySerializer(report_activity)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        profile = self.get_profile(request)

        data = request.data
        data.update({ "profile": profile.pk })

        activity = Activity.objects.filter(
            profile=profile,
            pk=request.data.get("activity_id")
        )

        if not activity:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReportActivitySerializer(data=request.data)

        if serializer.is_valid():

            report_already_done = ReportActivity.objects.filter(
                activity=request.data.get("activity_id"),
                profile=profile,
                created_at__contains=datetime.today().strftime("%Y-%m-%d")
            )

            if report_already_done:
                return Response({"detail": "Report has already been made for this activity today."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        profile = self.get_profile(request)

        report_activity = get_object_or_404(ReportActivity.objects.filter(profile=profile), pk=pk)
        serializer = ReportActivitySerializer(report_activity, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        profile = self.get_profile(request)

        report_activity = get_object_or_404(ReportActivity.objects.filter(profile=profile), pk=pk)
        report_activity.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=["get"], detail=False)
    def get_pending_today(self, request):
        profile = self.get_profile(request)
        
        today_reports = ReportActivity.objects.filter(
            profile=profile,
            created_at__contains=datetime.today().strftime("%Y-%m-%d")
        )

        activities = Activity.objects.filter(
            profile=profile,
            until__gte=datetime.today()
        )
        
        def filter_by_recurrence(recurrence):
            weekday = datetime.today().isoweekday()

            if recurrence in ["everyday"]:
                return True
            
            elif recurrence in ["week"]:
                if weekday in [1, 2, 3, 4, 5]:
                    return True

            elif recurrence in ["weekend"]:
                if weekday in [0, 6]:
                    return True
                
            return False
        
        filtered_activities_by_recurrence = [
            activity for activity in activities 
            if filter_by_recurrence(activity.recurrence)
        ]

        reported_activities = [report.activity for report in today_reports]

        pending_activities = [
            activity for activity in filtered_activities_by_recurrence 
            if activity not in reported_activities 
        ]

        serializer = ActivitySerializer(pending_activities, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_report_history_today(self, request):
        profile = self.get_profile(request)

        today_beginning = datetime.today().replace(hour=0, minute=0, second=0)

        reports = ReportActivity.objects.filter(
            profile=profile,
            created_at__gte=today_beginning
        ).order_by("-created_at")

        serializer = ReportActivitySerializer(reports, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_report_history(self, request):
        profile = self.get_profile(request)

        reports = ReportActivity.objects.filter(
            profile=profile,
        ).order_by("-created_at")

        paginator = PageNumberPagination()
        # paginator.page_size = 10
        page = paginator.paginate_queryset(reports, request)

        serializer = ReportActivitySerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)