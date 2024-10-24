from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Users.models import User




class TokenObtainSerializer(TokenObtainPairSerializer):
    # Custom Token Obtain Serializer that inherits from TokenObtainPairSerializer
    
    @classmethod
    def get_token(cls, user):
        # Override the get_token method to add custom claims to the token
        
        # Call the parent class's get_token method to get the default token
        token = super().get_token(user)
        
        # Add custom claims to the token
        # User custom claims
        token['username'] = user.username  # Add the user's username to the token
        token['email'] = user.email  # Add the user's email to the token
        token['phone'] = user.phone  # Add the user's phone to the token
        token['user_type'] = user.user_type  # Add the user's type to the token
        token['joined_date'] = str(user.joined_date)  # Add the user's joined date to the token
        
        # User profiles claims
        token['full_name'] = user.user_profile.full_name  # Add the user's first name to the token
        token['bio'] = user.user_profile.bio  # Add the user's bio to the token
        
        # Return the token with the added custom claims
        return token




class UserLoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(
        write_only=True,
        required=True
    )
    
    password = serializers.CharField(
        validators=[validate_password],
        write_only=True,
        required=True
    )