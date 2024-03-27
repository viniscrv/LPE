from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from activities.models import ReportActivity
from profiles.models import Profile
from datetime import timedelta

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

        return Response(most_performed, status=status.HTTP_200_OK)
    
    @action(methods=["get"], detail=True)
    def get_best_streak(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        reports = ReportActivity.objects.filter(profile=profile).order_by("completed_at")

        print("reports", reports)

        streaks = {}

        for report in reports:
            activity = report.activity

            # TODO: fazer para as outras recorrencias
            if activity.recurrence in ["everyday"]:
                if activity.name not in streaks:
                    streaks[activity.name] = { "streak": 1, "previous_date": report.completed_at }

                    continue

                expected_next_day = streaks[activity.name]["previous_date"] + timedelta(days=1)

                if report.completed_at.day == expected_next_day.day:
                    streaks[activity.name]["streak"] += 1
                    streaks[activity.name]["previous_date"] = report.completed_at

        best_streak = {}

        for activity_name, streak in streaks.items():
            if not best_streak:
                best_streak[activity_name] = streak["streak"]

            for top_activity, top_streak in best_streak.items():
                if streak["streak"] > top_streak:
                    del best_streak[top_activity]
                    
                    best_streak[activity] = streak["streak"]

        return Response(best_streak, status=status.HTTP_200_OK)