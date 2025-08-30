from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, create_checkout_session, StripeWebhookView
from django.urls import path

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('webhook/', StripeWebhookView.as_view(), name='webhook'),
]
urlpatterns += router.urls
