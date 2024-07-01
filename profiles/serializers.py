from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "first_name", "last_name", "username", "email", "biography"]

    first_name = serializers.CharField(
        max_length=155, 
        source="user.first_name", 
        read_only=True
    )

    last_name = serializers.CharField(
        max_length=155, 
        source="user.last_name", 
        read_only=True
    )

    username = serializers.CharField(
        max_length=155, 
        source="user.username", 
        read_only=True
    )

    email = serializers.CharField(
        max_length=155, 
        source="user.email", 
        read_only=True
    )

read_only=False
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user