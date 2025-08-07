from rest_framework import serializers
from .models import Organizer

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['id', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}