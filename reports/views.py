from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from activities.models import ReportActivity
from profiles.models import Profile

class ReportActivities(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=True)
    def get_most_performed_activity(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)
        
        reports_count = {}

        reports = ReportActivity.objects.filter(profile=profile)

        for report in reports:
            report_activity = report.activity

            if report_activity not in reports_count:
                reports_count[report_activity.name] = 0
            
            reports_count[report_activity.name] += 1

        most_performed = {}

        for activity, count in reports_count.items():
            if not most_performed:
                most_performed[activity] = count

            for top_activity, top_count in most_performed.items():
                if count > top_count:
                    del most_performed[top_activity]
                    
                    most_performed[activity] = count

        print(most_performed)

        return Response(most_performed, status=status.HTTP_200_OK)

