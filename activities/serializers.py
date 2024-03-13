from rest_framework import serializers
from .models import Activity, ReportActivity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["id", "name", "recurrence", "until", "created_at", "updated_at"]

class ReportActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportActivity
        fields = ["id", "activity", "effort_perception", "completed", "completed_at"]

    completed_at = serializers.DateTimeField(read_only=True)