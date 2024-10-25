from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework import status 

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import User

from .serializers import TokenObtainSerializer, UserLoginSerializer, UserRegisterSerializer



class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer
    
    

class UserLoginView(APIView):
    """
    API View for user login
    """
    def post(self, request):
        """
        Handle POST request for user login
        """
        # Check if the user is not already authenticated
        if request.user.is_authenticated == False:  # Simplified the condition
            # Create a serializer instance with the request data
            serializer = UserLoginSerializer(data=request.data)
            
            # Validate the serializer data
            if serializer.is_valid(raise_exception=True):
                # Authenticate the user using the phone and password
                user = authenticate(phone=serializer.validated_data['phone'], password=serializer.validated_data['password'])
                
                # Check if the user is authenticated
                if user:
                    # Check if the user account is active
                    if user.is_active:
                        # Generate a refresh token for the user
                        token = RefreshToken.for_user(user)
                        # Return the refresh and access tokens in the response
                        return Response(
                            {'refresh': str(token), 'access': str(token.access_token)},
                            status=status.HTTP_200_OK
                        )
                    else:
                        # Return an error response if the user account is disabled
                        return Response(
                            {'Detail': 'User account is disabled'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                else:
                    # Return an error response if the username or password is invalid
                    return Response(
                        {'Detail': 'Invalid phone or password'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Return an error response if the serializer validation fails
                return Response(
                    {'Detail': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Return an error response if the user is already logged in
            return Response(
                {'Detail': 'You are already logged in'},
                status=status.HTTP_400_BAD_REQUEST
            )



class UserRegisterView(APIView):
    """
    API View for user registration
    """
    def post(self, request):
        """
        Handle POST request for user registration
        """
        # Check if the user is not already authenticated
        if request.user.is_authenticated == False:  # Simplified the condition
            # Create a serializer instance with the request data
            serializer = UserRegisterSerializer(data=request.data)
            
            # Validate the serializer data
            if serializer.is_valid(raise_exception=True):
               # Create a new user
                user = User.objects.create_user(
                    email = serializer.validated_data["email"],
                    phone = serializer.validated_data["phone"],
                    username = serializer.validated_data["username"],
                    password = serializer.validated_data["password"],
                    user_type = serializer.validated_data["user_type"]
                )
                user.save()
                # Authenticate the user
                authenticate(user)
                # Generate a refresh token for the user
                token = RefreshToken.for_user(user)
                # Return a success response with the tokens
                return Response(
                    {
                        'Detail': {
                            'Message': 'User created successfully',  # Return a success message
                            'Token': {
                                'refresh': str(token),  # Return the refresh token
                                'access': str(token.access_token)  # Return the access token
                            }
                        }
                    }, status=status.HTTP_201_CREATED
                )
            else:
                # Return an error response if the serializer validation fails
                return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return an error response if the user is already logged in
            return Response({'Detail': 'You are already logged in'}, status=status.HTTP_400_BAD_REQUEST)
