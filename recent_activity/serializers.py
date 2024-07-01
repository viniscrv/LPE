from rest_framework import serializers
from .models import RecentActivity

class RecentActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentActivity
        fields = ["profile", "activity", "type"]