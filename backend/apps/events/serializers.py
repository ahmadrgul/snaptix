from rest_framework import serializers
from .models import Event, Ticket

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'organizer')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
