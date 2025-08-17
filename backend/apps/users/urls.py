from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizerViewSet

router = DefaultRouter()
router.register(r'organizers', OrganizerViewSet, basename='organizer')

urlpatterns = router.urls