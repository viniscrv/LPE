from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from activities.models import ReportActivity
from activities.serializers import ActivitySerializer
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
                reports_count[report_activity] = 0
            
            reports_count[report_activity] += 1

        most_performed = {}
        total_performed_count = 0 

        for activity, activity_count in reports_count.items():
            if not most_performed:
                most_performed["acttivity"] = activity
                most_performed["count"] = activity_count

            total_performed_count += activity_count

            if activity_count > most_performed["count"]:
                most_performed["activity"] = activity
                most_performed["count"] = activity_count

        average_count = total_performed_count / len(reports_count.keys())

        try:
            percentage_about_average = (most_performed["count"] / average_count) * 100
        except ZeroDivisionError:
            percentage_about_average = 0.0

        serializer = ActivitySerializer(most_performed["activiy"])
        most_performed["activity"] = serializer.data
        
        most_performed.update({"percentage": percentage_about_average})

        return Response(most_performed, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def get_best_streak(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        reports = ReportActivity.objects.filter(profile=profile).order_by("completed_at")

        streaks = {}

        def get_next_day(previous_date, recurrence):
            previous_date_weekday = previous_date.isoweekday()

            if recurrence in ["everyday"]:
                return previous_date + timedelta(days=1)
            
            elif recurrence in ["week"]:
                if previous_date_weekday in [1, 2, 3, 4]:
                    return previous_date + timedelta(days=1)
                
                len_full_week = 7
                days_until_next_monday = previous_date_weekday - len_full_week

                return previous_date + timedelta(days=days_until_next_monday)
                
            elif recurrence in ["weekend"]:
                if previous_date_weekday in [6]:
                    return previous_date + timedelta(days=1)
                
                len_full_week = 7
                days_until_next_saturday = previous_date_weekday - len_full_week

                return previous_date + timedelta(days=days_until_next_saturday)
                
            return previous_date
        
        for report in reports:
            activity = report.activity

            if activity not in streaks:
                streaks[activity] = { "streak": 1, "previous_date": report.completed_at }

                continue

            expected_next_day = get_next_day(
                streaks[activity]["previous_date"], activity.recurrence
            )

            if report.completed_at.day == expected_next_day.day:
                streaks[activity]["streak"] += 1
                streaks[activity]["previous_date"] = report.completed_at

        best_streak = {}

        for activity, streak in streaks.items():
            if not best_streak:
                best_streak["activity"] = activity
                best_streak["streak"] = streak["streak"]

            if streak["streak"] > best_streak["streak"]:
                best_streak["activity"] = activity
                best_streak["streak"] = streak["streak"]

        serializer = ActivitySerializer(best_streak["activity"])
        best_streak["activity"] = serializer.data

        return Response(best_streak, status=status.HTTP_200_OK)
    
    # TODO: nome paia
    @action(methods=["get"], detail=True)
    def get_edges_difficulty_activities_to_perform(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        reports = ReportActivity.objects.filter(profile=profile)

        effort_history = {}

        for report in reports:
            activity = report.activity

            if activity not in effort_history:
                effort_history[activity] = []

            effort_history[activity].append(report.effort_perception)

        edges_activity = {
            "highest": {},
            "lowest": {},
        }

        def fill_edge(level, activity_data):
            fields = ["activity", "average_effort"]

            for field in fields:
                edges_activity[level][field] = activity_data[field]

        for activity, efforts in effort_history.items():
            average_effort = sum(
                [int(effort) for effort in efforts]
            ) / len(efforts)

            activity_data = {
                "activity": activity,
                "average_effort": average_effort,
            }
            
            if not edges_activity["highest"] or not edges_activity["lowest"]:
                fill_edge(level="highest", activity_data=activity_data)
                fill_edge(level="lowest", activity_data=activity_data)

            if average_effort > edges_activity["highest"]["average_effort"]:
                fill_edge(level="highest", activity_data=activity_data)
            
            if average_effort < edges_activity["lowest"]["average_effort"]:
                fill_edge(level="lowest", activity_data=activity_data)

        for level in edges_activity:
            serializer = ActivitySerializer(edges_activity[level]["activity"])
            edges_activity[level]["activity"] = serializer.data

        return Response(edges_activity, status=status.HTTP_200_OK)