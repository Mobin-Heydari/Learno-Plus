from rest_framework.views import APIView, Response
from rest_framework import status 

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import TokenObtainSerializer



class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer