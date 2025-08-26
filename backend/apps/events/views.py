from rest_framework import viewsets
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import MultiPartRenderer, HTMLFormRenderer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    owner_field = 'organizer'
    # renderer_classes = [MultiPartRenderer, HTMLFormRenderer]

    def get_queryset(self):
        qs = Event.objects.all()
        user = self.request.user
        
        if user.is_authenticated:
            if user.is_staff:
                # staff can access all events
                return qs
            if user.role == 'organizer':
                # organizers can access their own events
                return qs.filter(organizer=user.organizer)
            
        if self.action == 'list':
            # public can access only listed events unless they direclty retrieve a specific event
            qs = qs.filter(is_listed=True)

        # public can access only the events that are not draft
        return qs.exclude(status='draft')

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.is_authenticated and user.role == 'organizer':
            # only authenticated organizers can create events
            serializer.save(organizer=self.request.user.organizer)
            
        else:
            raise PermissionDenied("Only authenticated organizers can create events.")

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrReadOnly]
    owner_field = 'event.organizer'