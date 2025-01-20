from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from django.contrib.auth.hashers import make_password
from .models import ClubUser, Court, Reservation


class ClubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubUser
        fields = [
            'id', 'username', 'name', 'last_name', 'email',
            'phone', 'membership_type', 'address', 'password',
        ]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CourtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['user']  # Ensure the 'user' field is not required from the frontend

    def validate(self, data):
        court = data['court']
        date = data['date']
        start_time = data['start_time']
        end_time = data['end_time']

        # Check for overlapping reservations
        overlapping_reservations = Reservation.objects.filter(
            court=court,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if overlapping_reservations.exists():
            raise ValidationError("The court is already reserved for the selected time slot.")

        return data

    def create(self, validated_data):
        # Add the authenticated user to the reservation
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
