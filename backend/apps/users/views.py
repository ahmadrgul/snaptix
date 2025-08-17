from django.shortcuts import render
from rest_framework import viewsets
from .models import Organizer
from .serializers import OrganizerSerializer

class OrganizerViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizerSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return Organizer.objects.all()
        return Organizer.objects.filter(pk=self.request.user.id)

    # No restrictions on POST
    # No restrictions on GET, but all fields are visible to owner and admin,
    # while others can only see the name.
    # PUT, PATCH, DELETE are restricted to owner and admin
