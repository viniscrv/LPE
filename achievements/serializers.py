from rest_framework import serializers
from .models import Achievement
from activities.models import Activity
from activities.serializers import ActivitySerializer

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "profile", "activity", "activity_id", "type", "created_at"]

    activity = ActivitySerializer(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), source='activity', write_only=True)