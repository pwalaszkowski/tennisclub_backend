from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import ClubUser

class ClubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubUser
        fields = ['username', 'name', 'last_name', 'email', 'phone', 'membership_type', 'address', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
