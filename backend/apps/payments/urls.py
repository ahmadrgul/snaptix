from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, create_checkout_session
from django.urls import path

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('api/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
]
urlpatterns += router.urls
