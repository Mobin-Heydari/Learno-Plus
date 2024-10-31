from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from .models import UserProfile
from .serializers import UserProfileSerializer

from Users.models import User
from .permissions import IsOwnerOrReadOnly




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
        # Getting the user by username (pk)
        user = get_object_or_404(User, username=pk)
        # Getting profile queryset by user
        queryset = get_object_or_404(UserProfile, user=user)
        # Serializing the user profile queryset
        serializer = UserProfileSerializer(instance=queryset)
        # Returning the serialized data with http 200 status code
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        # Get the user instance by username (pk)
        user = get_object_or_404(User, username=pk)
        # Get the UserProfile instance associated with the user
        queryset = get_object_or_404(UserProfile, user=user)

        # Check if the requesting user is authenticated
        if request.user.is_authenticated:
            # Check object permissions using the permission classes
            self.check_object_permissions(request, queryset)

            # Update the profile instance using the UserProfileSerializer
            serializer = UserProfileSerializer(queryset, data=request.data, partial=True)

            # If the data is valid, update the instance and return a 200 OK response
            if serializer.is_valid(raise_exception=True):
                serializer.save()  # This will call the update method in the serializer
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                # Return a 400 Bad Request response if the data is invalid
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Return a 401 Unauthorized response if the user is not authenticated
            return Response(
                {
                    'Detail': 'You are not authenticated.'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
