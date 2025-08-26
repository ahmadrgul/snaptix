from rest_framework import viewsets
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from rest_framework.renderers import MultiPartRenderer, HTMLFormRenderer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # renderer_classes = [MultiPartRenderer, HTMLFormRenderer]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer