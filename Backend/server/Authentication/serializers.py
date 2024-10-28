from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string

from rest_framework import serializers
from rest_framework import validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import User

from . models import OneTimePassword

from random import randint



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
    
    phone = serializers.CharField(
        write_only=True,
        required=True
    )
    
    password = serializers.CharField(
        validators=[validate_password],
        write_only=True,
        required=True
    )




class OneTimePasswordSerializer(serializers.Serializer):
    
    """
    Serializer for user registration
    """
    
    # Email field with unique validator to ensure email is not already in use
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )
    
    # Phone field with unique validator to ensure phone is not already in use
    phone = serializers.CharField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )
    
    # Username field with unique validator to ensure username is not already in use
    username = serializers.CharField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )
    
    # Password field with custom validator and write-only access
    password = serializers.CharField(
        validators=[validate_password],
        write_only=True,
        required=True
    )

    # Password confirmation field with write-only access
    password_conf = serializers.CharField(
        validators=[validate_password],
        write_only=True,
        required=True
    )

    # User type field with write-only access
    user_type = serializers.CharField(
        write_only=True,
        required=True
    )
    
    
    def validate(self, attrs):
        """
        Validate the serializer data
        """
        # Check if the password and password confirmation match
        if attrs['password'] == attrs['password_conf']:
            # Check if the password length is between 8 and 16 characters
            if len(attrs['password']) >= 8 and len(attrs['password']) <= 16:
                return attrs
            else:
                raise serializers.ValidationError({"Detail": "Password length should be between 8 to 16 characters."})
        else:
            raise serializers.ValidationError({"Detail": "Passwords fields didn't match."})
        
        
    def create(self, validated_data):
        
        # Generate a random code and token
        code = randint(100000, 999999)
        token = get_random_string(100)
        
        # Create a new OneTimePassword object with the validated data
        otp = OneTimePassword.objects.create(
            email = validated_data['email'],
            username = validated_data['username'],
            phone = validated_data['phone'],
            user_type = validated_data['user_type'],
            password = validated_data['password'],
            token = token,
            code = code
        )
        
        # Save the OneTimePassword object to the database
        otp.save()
        
        # Returning the otp data
        return {
            'token': token,
            'code': code
        }
        
        
class UserRegisterSerializer(serializers.Serializer):
    
    code  = serializers.CharField(max_length=6, min_length=6, required=True)
    
    
    def create(self, validated_data, token):

        
        otp = OneTimePassword.objects.get(token=token)
        
        # Create a new user using the OTP details
        user = User.objects.create_user(
            email=otp.email,
            username=otp.username,
            phone=otp.phone,
            password=otp.password,
            user_type=otp.user_type
        )
        
        user.save()

        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)

        # Return user data and tokens
        return {
            'user': {
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                # Add any other user fields you want to return
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }