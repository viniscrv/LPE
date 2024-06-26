from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

class ProfileView(ViewSet):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        user_id = request.user.id

        if request.user.is_anonymous:
            user_serializer = UserSerializer(data=request.data)

            if not user_serializer.is_valid():
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user_serializer.save()
            user_id = user_serializer.data.get("id")

        user_already_has_profile = Profile.objects.filter(user=user_id)

        if user_already_has_profile:
            return Response({"detail": "User already has been created."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        data.update({ "user": user_id })

        profile_serializer = ProfileSerializer(data=data)

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        data = request.data

        profile = get_object_or_404(Profile, user=request.user.id)
        serializer = ProfileSerializer(profile, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["patch"], detail=True)
    def edit_password(self, request):
        data = request.data

        User = get_user_model()

        user = User.objects.get(pk=request.user.id)

        if user:
            user.set_password(data.get("password"))
            user.save()
            
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)