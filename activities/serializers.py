from rest_framework import serializers
from .models import ActivityGroup, Activity, ReportActivity

class ActivityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityGroup
        fields = ["id", "profile", "name", "description"]

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["id", "profile", "activity_group_id", "activity_group", "name", "recurrence", "until", "created_at", "updated_at"]

    activity_group = ActivityGroupSerializer(read_only=True)
    activity_group_id = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), source='activity_group', write_only=True)

class ReportActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportActivity
        fields = ["id", "profile", "activity_id", "activity", "effort_perception", "completed", "completed_at"]
    
    activity = ActivitySerializer(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), source='activity', write_only=True)
