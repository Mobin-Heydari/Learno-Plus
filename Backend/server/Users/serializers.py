from rest_framework import serializers

from .models import User



class UserSerializer(serializers.ModelSerializer):
    # Define the fields to be serialized
    class Meta:
        model = User
        fields = '__all__'