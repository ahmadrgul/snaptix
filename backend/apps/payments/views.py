import os
import stripe
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from apps.events.models import Event, Ticket
from rest_framework import viewsets
from .serializers import PaymentSerializer
from .models import Payment

# Load environment variables from a .env file. Remove these lines in production.
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


@api_view(['POST'])
def create_checkout_session(request):
    payment_id = request.data.get('payment_id')
    if not payment_id:
        return Response({'payment_id': ['This field is required']}, status=400)

    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return Response({'details': 'Payment not found'}, status=404)

    if not payment.status == 'pending' or not payment.ticket.status == 'pending':
        return Response({'details': 'Payment or Ticket not in a valid state for checkout'}, status=400)

    event = payment.ticket.event

    session = stripe.checkout.Session.create(
        mode = 'payment',
        line_items = [{
            'price': event.stripe_price_id,
            'quantity': 1,
        }],
        success_url = 'https://example.com/success',
        cancel_url = 'https://example.com/cancel',
        metadata={
            'payment_id': payment.id,
            'ticket_id': payment.ticket.id,
            'event_id': event.id,
        }
    )

    return Response({'id': session.id})

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return Response(status=400)
        except stripe.error.SignatureVerificationError:
            return Response(status=400)
        
        if event['type'] == 'checkout.session.completed':
            payment_id = event['data']['object']['metadata']['payment_id']
            try:
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'completed'
                payment.stripe_payment_intent_id = event['data']['object']['payment_intent']
                payment.save()
            except Payment.DoesNotExist:
                return Response(status=404)
            
            ticket_id = event['data']['object']['metadata']['ticket_id']
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.status = 'paid'
                ticket.save()
            except Ticket.DoesNotExist:
                return Response(status=404)
            
            event_id = event['data']['object']['metadata']['event_id']
            try:
                event_instance = Event.objects.get(id=event_id)
                event_instance.sold_tickets += 1
                event_instance.save()
            except Event.DoesNotExist:
                return Response(status=404)

        return Response(status=200)
