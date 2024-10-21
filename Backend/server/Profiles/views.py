from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from .models import UserProfile
from .serializers import UserProfileSerializer

from Users.models import User



class UserProfileViewSet(ViewSet):
    
    # List method for profiles
    def list(self, request):
        # Getting profiles queries 
        queryset = UserProfile.objects.all()
        # Serializing the queryset data 
        serializer = UserProfileSerializer(instance=queryset, many=True)
        # Returning the serialized data with http 200 status code
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Retrieve method for profiles
    def retrieve(self, request, pk):
        # Getting the user by pk that includes the username
        user = get_object_or_404(User, username=pk)
        # Getting profile queryset by user
        queryset = get_object_or_404(UserProfile, user=user)
        # Serializing the user profile queryset
        serializer = UserProfileSerializer(instance=queryset)
        # Returning the serialized data with http 200 status code
        return Response(serializer.data, status=status.HTTP_200_OK)
