from rest_framework import serializers
from .models import ActivityGroup, Activity, ReportActivity

class ActivityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityGroup
        fields = ["id", "profile", "name", "description"]

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["id", "profile", "activity_group", "name", "recurrence", "until", "created_at", "updated_at"]

class ReportActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportActivity
        fields = ["id", "profile", "activity", "effort_perception", "completed", "completed_at"]

    completed_at = serializers.DateTimeField(read_only=True)