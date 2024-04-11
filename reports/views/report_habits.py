from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from activities.models import ReportActivity
from profiles.models import Profile
from datetime import datetime, timedelta
from django.db.models import Q
from activities.serializers import ActivitySerializer

class ReportHabits(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=True)
    def get_habit_formation_progress(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        def get_predecessor_day(previous_date, recurrence):
            previous_date_weekday = previous_date.isoweekday()

            if recurrence in ["everyday"]:
                return previous_date - timedelta(days=1)
            
            elif recurrence in ["week"]:
                if previous_date_weekday in [1, 2, 3, 4]:
                    return previous_date - timedelta(days=1)
                
                len_full_week = 7
                days_until_next_monday = previous_date_weekday - len_full_week

                return previous_date - timedelta(days=days_until_next_monday)
                
            elif recurrence in ["weekend"]:
                if previous_date_weekday in [6]:
                    return previous_date - timedelta(days=1)
                
                len_full_week = 7
                days_until_next_saturday = previous_date_weekday - len_full_week

                return previous_date - timedelta(days=days_until_next_saturday)
                
            return previous_date

        reports = ReportActivity.objects.filter(profile=profile).order_by("-completed_at")

        streaks = {}

        for report in reports:
            activity = report.activity

            if activity not in streaks:
                streaks[activity] = {
                    "streak": 1, 
                    "previous_date": report.completed_at,
                    "last_report": report.completed_at
                }

                continue

            expected_predecessor_day = get_predecessor_day(
                streaks[activity]["previous_date"], activity.recurrence
            )

            if report.completed_at.day == expected_predecessor_day.day:
                streaks[activity]["streak"] += 1
                streaks[activity]["previous_date"] = report.completed_at

        # TODO: fazer para outras recorrencias
        recent_reports = ReportActivity.objects.filter(
            Q(profile=profile),
            Q(created_at__contains=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")) |
            Q(created_at__contains=(datetime.today()).strftime("%Y-%m-%d")) 
        )

        recent_activities = [report.activity for report in recent_reports]
        
        streaks_in_progress = [
            streaks[streak_activity] for streak_activity 
            in streaks.keys() 
            if streak_activity in recent_activities
        ]

        streaks_in_progress = []

        for streak_activity, data in streaks.items():
            if streak_activity in recent_activities:
                
                serializer = ActivitySerializer(streak_activity)
                data["activity"] = serializer.data

                # TODO: globalizar na classe o 66
                data["days_until_habit"] = 66 - data["streak"]

                streaks_in_progress.append(data)

        return Response(streaks_in_progress, status=status.HTTP_200_OK)
    
    @action(methods=["get"], detail=True)
    def get_habit_disintegration_progress(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        def get_predecessor_day(previous_date, recurrence):
            previous_date_weekday = previous_date.isoweekday()

            if recurrence in ["everyday"]:
                return previous_date - timedelta(days=1)
            
            elif recurrence in ["week"]:
                if previous_date_weekday in [1, 2, 3, 4]:
                    return previous_date - timedelta(days=1)
                
                len_full_week = 7
                days_until_next_monday = previous_date_weekday - len_full_week

                return previous_date - timedelta(days=days_until_next_monday)
                
            elif recurrence in ["weekend"]:
                if previous_date_weekday in [6]:
                    return previous_date - timedelta(days=1)
                
                len_full_week = 7
                days_until_next_saturday = previous_date_weekday - len_full_week

                return previous_date - timedelta(days=days_until_next_saturday)
                
            return previous_date

        reports = ReportActivity.objects.filter(profile=profile).order_by("-completed_at")

        streaks = {}

        for report in reports:
            activity = report.activity

            if activity not in streaks:
                streaks[activity] = {
                    "streak": 1, 
                    "previous_date": report.completed_at,
                    "last_report": report.completed_at
                }

                continue

            expected_predecessor_day = get_predecessor_day(
                streaks[activity]["previous_date"], activity.recurrence
            )

            if report.completed_at.day == expected_predecessor_day.day:
                streaks[activity]["streak"] += 1
                streaks[activity]["previous_date"] = report.completed_at

        # TODO: fazer para outras recorrencias
        recent_reports = ReportActivity.objects.filter(
            Q(profile=profile),
            Q(created_at__contains=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")) |
            Q(created_at__contains=(datetime.today()).strftime("%Y-%m-%d")) 
        )

        recent_activities = [report.activity for report in recent_reports]
        
        streaks_in_progress = [
            streaks[streak_activity] for streak_activity 
            in streaks.keys() 
            if streak_activity in recent_activities
        ]

        streaks_in_progress = []

        for streak_activity, data in streaks.items():
            if streak_activity not in recent_activities:

                serializer = ActivitySerializer(streak_activity)
                data["activity"] = serializer.data
                # TODO: globalizar na classe o 66
                # TODO: ver se remover tzinfo pode dar problema
                data["days_until_disintegrate_habit"] = abs(
                    (
                        datetime.today() - data["last_report"].replace(tzinfo=None)
                    ).days - 66
                )

                streaks_in_progress.append(data)

        return Response(streaks_in_progress, status=status.HTTP_200_OK)