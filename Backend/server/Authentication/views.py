from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView, Response
from rest_framework import status 

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import User

from .serializers import TokenObtainSerializer, UserLoginSerializer, UserRegisterSerializer, OneTimePasswordSerializer

from .models import  OneTimePassword






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



class OneTimePasswordView(APIView):
    """
        API view to generate a one-time password 
    """
    def post(self, request):
        """
        Handle POST request for one-time password auth
        """
        # Check if the user is not authenticated
        if not request.user.is_authenticated:
            # Create an instance of the serializer with the request data
            serializer = OneTimePasswordSerializer(data=request.data)
            
            # Validate the serializer data
            if serializer.is_valid(raise_exception=True):
                # Call the create method with the validated data
                otp_data = serializer.create(validated_data=serializer.validated_data)  # Save and get the OTP data
                
                # Return a success response with the OTP details
                return Response(
                    {
                        'Detail': {
                            'Message': 'Otp created successfully',
                            'token': otp_data['token'],  # Assuming otp_data has a token attribute
                            'code': otp_data['code']       # Assuming otp_data has a code attribute
                        }
                    }, status=status.HTTP_201_CREATED
                )
            else:
                # Return an error response if the serializer validation fails
                return Response({'Detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return an error response if the user is already logged in
            return Response({'Detail': 'You are already logged in'}, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(APIView):
    """
    API View to handle OneTimePassword verification and user creation
    """
    def post(self, request, token):
        """
        Handle POST request to verify OneTimePassword and create user
        """
        # Check if the user is not authenticated
        if not request.user.is_authenticated:
            # Get the OneTimePassword object from the database using the provided token
            otp = get_object_or_404(OneTimePassword, token=token)
            if otp:
                # Serialize the request data using the UserRegisterSerializer
                serializer = UserRegisterSerializer(data=request.data, context={'otp_token' : otp.token})
                if serializer.is_valid(raise_exception=True):
                    # Saving the user data and getting user and tokens
                    user_data = serializer.create(validated_data=serializer.validated_data, token=token)

                    # Return a success response with user data and tokens
                    return Response(
                        {
                            'Detail': {
                                'Message': 'User  created successfully',
                                'User': user_data['user'],
                                'Token': user_data['tokens']
                            }
                        }, status=status.HTTP_201_CREATED
                    )  
                else:
                    # Return an error response if the serializer is invalid
                    return Response(
                        {'Detail': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Return an error response if the OTP does not exist
                return Response(
                    {'Detail': 'OTP does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Return an error response if the user is already authenticated
            return Response(
                {'Detail': 'You are already authenticated'},
                status=status.HTTP_400_BAD_REQUEST
            )