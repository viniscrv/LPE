from rest_framework import serializers
from .models import RecentActivity
from activities.serializers import ActivitySerializer
from activities.models import Activity

class RecentActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentActivity
        fields = ["profile", "activity" ,"activity_id", "type", "created_at"]

    activity = ActivitySerializer(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), source='activity', write_only=True)