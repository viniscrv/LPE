from .models import Achievement
from .serializers import AchievementSerializer

def validate_and_create_new_achievements(profile, activity, type):
    achievements = Achievement.objects.filter(profile=profile, type=type)
    
    if achievements:
        last_achievement = achievements[-1]

        if last_achievement.activity == activity:
            return
        
    achievement_data = {
        "profile": profile,
        "activity": activity,
        "type": type
    }

    serializer = AchievementSerializer(data=achievement_data)

    if serializer.is_valid():
        serializer.save()