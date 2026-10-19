from rest_framework import serializers
from .models import User, StoreMembership

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class StoreMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StoreMembership
        fields = ["id", "user", "store", "role"]