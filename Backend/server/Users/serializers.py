from rest_framework import serializers

from .models import User



class UserSerializer(serializers.ModelSerializer):
    # Define the fields to be serialized
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'joined_date', 'last_login', 'is_active', 'is_admin']