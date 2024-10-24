from rest_framework import serializers

from .models import UserProfile

from Users.serializers import UserSerializer



class UserProfileSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'full_name', 'image', 'user']
        
        
    def get_user(self, obj):
        
        serializer = UserSerializer(instance=obj.user)
        
        return serializer.data