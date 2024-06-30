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
from achievements.utils import validate_and_create_new_achievements

class ReportHabits(ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_all_streaks(self, profile):
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

        return streaks

    @action(methods=["get"], detail=True)
    def get_habit_formation_progress(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        streaks = self._get_all_streaks(profile)

        # TODO: fazer para outras recorrencias
        recent_reports = ReportActivity.objects.filter(
            Q(profile=profile),
            Q(created_at__contains=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")) |
            Q(created_at__contains=(datetime.today()).strftime("%Y-%m-%d")) 
        )

        recent_activities = [report.activity for report in recent_reports]
        
        streaks_in_progress = []

        for streak_activity, data in streaks.items():
            if streak_activity in recent_activities:
                
                serializer = ActivitySerializer(streak_activity)
                data["activity"] = serializer.data

                # TODO: globalizar na classe o 66
                data["days_until_habit"] = 66 - data["streak"]

                try:
                    data["percentage_progress"] = (data["days_until_habit"] / 66) * 100 

                except ZeroDivisionError:
                    data["percentage_progress"] = 0.0

                streaks_in_progress.append(data)

        return Response(streaks_in_progress, status=status.HTTP_200_OK)
    
    @action(methods=["get"], detail=True)
    def get_habit_disintegration_progress(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        streaks = self._get_all_streaks(profile)

        disintegrate_habits = []

        for streak_activity, data in streaks.items():
            if streak_activity:

                if data["streak"] < 66:
                    continue

                diff_last_report_for_habit_mark = data["last_report"] - (datetime.today() - timedelta(days=66))

                if diff_last_report_for_habit_mark <= 0:
                    continue

                serializer = ActivitySerializer(streak_activity)
                data["activity"] = serializer.data
                data["days_until_disintegrate_habit"] = diff_last_report_for_habit_mark

                disintegrate_habits.append(data)

        return Response(disintegrate_habits, status=status.HTTP_200_OK)
    
    @action(methods=["get"], detail=True)
    def get_current_habits(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        streaks = self._get_all_streaks(profile)

        # TODO: fazer para outras recorrencias
        recent_reports = ReportActivity.objects.filter(
            Q(profile=profile),
            Q(created_at__contains=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")) |
            Q(created_at__contains=(datetime.today()).strftime("%Y-%m-%d")) 
        )

        recent_activities = [report.activity for report in recent_reports]
        
        current_habits = []

        for streak_activity, data in streaks.items():
            if streak_activity in recent_activities:

                if data["streak"] < 66:
                    continue

                serializer = ActivitySerializer(streak_activity)
                data["activity"] = serializer.data

                current_habits.append(data)

        return Response(current_habits, status=status.HTTP_200_OK)