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
    
    
    def update(self, instance, validated_data):
        # Update the UserProfile fields
        instance.bio = validated_data.get('bio', instance.bio)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.image = validated_data.get('image', instance.image)

        # Save the changes to the UserProfile instance
        instance.save()
        
        return instance