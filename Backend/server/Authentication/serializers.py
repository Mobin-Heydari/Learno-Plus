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
        token['full_name'] = user.user_profile.full_name  # Add the user's full name to the token
        token['bio'] = user.user_profile.bio  # Add the user's bio to the token
        
        # Return the token with the added custom claims
        return token


class UserLoginSerializer(serializers.Serializer):
    # Serializer for user login
    
    phone = serializers.CharField(
        write_only=True,  # This field is only used for input, not output
        required=True  # This field is required
    )
    
    password = serializers.CharField(
        validators=[validate_password],  # Validate the password using Django's password validation
        write_only=True,  # This field is only used for input, not output
        required=True  # This field is required
    )


class OneTimePasswordSerializer(serializers.Serializer):
    """
    Serializer for user registration
    """
    
    # Email field with unique validator to ensure email is not already in use
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(queryset=User .objects.all())  # Ensure email is unique in User model
        ]
    )
    
    # Phone field with unique validator to ensure phone is not already in use
    phone = serializers.CharField(
        validators=[
            validators.UniqueValidator(queryset=User .objects.all())  # Ensure phone is unique in User model
        ]
    )
    
    # Username field with unique validator to ensure username is not already in use
    username = serializers.CharField(
        validators=[
            validators.UniqueValidator(queryset=User .objects.all())  # Ensure username is unique in User model
        ]
    )
    
    # Password field with custom validator and write-only access
    password = serializers.CharField(
        validators=[validate_password],  # Validate the password using Django's password validation
        write_only=True,  # This field is only used for input, not output
        required=True  # This field is required
    )

    # Password confirmation field with write-only access
    password_conf = serializers.CharField(
        validators=[validate_password],  # Validate the password using Django's password validation
        write_only=True,  # This field is only used for input, not output
        required=True  # This field is required
    )

    # User type field with write-only access
    user_type = serializers.CharField(
        write_only=True,  # This field is only used for input, not output
        required=True  # This field is required
    )
    
    
    def validate(self, attrs):
        """
        Validate the serializer data
        """
        # Check if the password and password confirmation match
        if attrs['password'] == attrs['password_conf']:
            # Check if the password length is between 8 and 16 characters
            if len(attrs['password']) >= 8 and len(attrs['password']) <= 16:
                return attrs  # Return validated attributes if all checks pass
            else:
                raise serializers.ValidationError({"Detail": "Password length should be between 8 to 16 characters."})
        else:
            raise serializers.ValidationError({"Detail": "Passwords fields didn't match."})
        
        
    def create(self, validated_data):
        # Generate a random code and token for one-time password
        code = randint(100000, 999999)  # Generate a random 6-digit code
        token = get_random_string(100)  # Generate a random token of length 100
        
        # Create a new OneTimePassword object with the validated data
        otp = OneTimePassword .objects.create(
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
        
        otp.get_expiration()  # Get the expiration time of the OTP
        
        # Returning the otp data
        return {
            'token': token,
            'code': code
        }
        
        
class UserRegisterSerializer(serializers.Serializer):
    # Serializer for user registration using one-time password
    
    code  = serializers.CharField(max_length=6, min_length=6, required=True)
    
    
    def validate(self, attrs):
        otp_token = self.context.get('otp_token')  # Get the OTP token from the context
        
        otp = OneTimePassword.objects.get(token=otp_token)  # Get the OneTimePassword object using the token
        
        if otp.status_validation() == 'ACT':  # Check if the OTP is active
            if otp.code == attrs['code']:  # Check if the provided code matches the OTP code
                return attrs  # Return validated attributes if all checks pass
            else:
                raise serializers.ValidationError({'code': 'Invalid OTP code.'})
        else:
            raise serializers.ValidationError('Inactive OTP')
    
    
    def create(self, validated_data, token):
        
        otp = OneTimePassword.objects.get(token=token)  # Get the OneTimePassword object using the token
        
        # Create a new user using the OTP details
        user = User.objects.create_user(
            email=otp.email,
            username=otp.username,
            phone=otp.phone,
            password=otp.password,
            user_type=otp.user_type
        )
        
        user.save()  # Save the user to the database
        
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