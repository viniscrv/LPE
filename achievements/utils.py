from .models import Achievement
from .serializers import AchievementSerializer

def validate_and_create_new_achievements(profile, activity, type):
    last_achievement = Achievement.objects.filter(profile=profile, type=type).order_by('-id')[:1]
    
    if last_achievement:
        if last_achievement[0].activity.id == activity:
            return
        
    achievement_data = {
        "profile": profile,
        "activity_id": activity,
        "type": type
    }

    serializer = AchievementSerializer(data=achievement_data)

    if serializer.is_valid():
        serializer.save()