from .serializers import RecentActivitySerializer

def create_recent_activity(profile, activity, type):
    type_map = {
        "create": "complete_report",
        "edit": "edit_report",
        "delete": "delete_report",
    }

    recent_activity_data = {
        "profile": profile,
        "activity": activity,
        "type": type_map.get(type, "complete_report")
    }

    serializer = RecentActivitySerializer(data=recent_activity_data)

    if serializer.is_valid():
        serializer.save()