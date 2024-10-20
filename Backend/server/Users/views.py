from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from . import serializers
from .models import User



class UserViewSet(ViewSet):
    """
    A ViewSet for handling user-related API requests.
    """
    
    def list(self, request):
        """
        Return a list of all users.
        """
        queryset = User.objects.all()
        
        serializer = serializers.UserSerializer(instance=queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        """
        Return a single user by username.
        """
        
        query = get_object_or_404(User, username=pk)
        
        serializer = serializers.UserSerializer(instance=query)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
