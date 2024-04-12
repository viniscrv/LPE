from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from activities.models import ReportActivity
from profiles.models import Profile
from rest_framework.response import Response
from rest_framework import status
from activities.serializers import ActivityGroupSerializer

class ReportGroupActivities(ViewSet):
    permission_classes = [IsAuthenticated]

    # TODO: nome paia
    @action(methods=["get"], detail=True)
    def get_edges_difficulty_group_activities_to_perform(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        reports = ReportActivity.objects.filter(profile=profile)

        effort_history = {}

        for report in reports:
            activity_group = report.activity.activity_group

            if activity_group not in effort_history:
                effort_history[activity_group] = []

            effort_history[activity_group].append(report.effort_perception)

        edges_activity_group = {
            "highest": {},
            "lowest": {},
        }

        def fill_edge(level, activity_group_data):
            fields = ["activity_group", "average_effort"]

            for field in fields:
                edges_activity_group[level][field] = activity_group_data[field]

        for activity_group, efforts in effort_history.items():
            average_effort = sum(
                [int(effort) for effort in efforts]
            ) / len(efforts)

            activity_group_data = {
                "activity_group": activity_group,
                "average_effort": average_effort,
            }
            
            if not edges_activity_group["highest"] or not edges_activity_group["lowest"]:
                fill_edge(level="highest", activity_group_data=activity_group_data)
                fill_edge(level="lowest", activity_group_data=activity_group_data)

            if average_effort > edges_activity_group["highest"]["average_effort"]:
                fill_edge(level="highest", activity_group_data=activity_group_data)
            
            if average_effort < edges_activity_group["lowest"]["average_effort"]:
                fill_edge(level="lowest", activity_group_data=activity_group_data)

        for level in edges_activity_group:
            serializer = ActivityGroupSerializer(edges_activity_group[level]["activity_group"])
            edges_activity_group[level]["activity_group"] = serializer.data

        return Response(edges_activity_group, status=status.HTTP_200_OK)