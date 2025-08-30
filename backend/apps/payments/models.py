import uuid
from django.db import models
from djmoney.models.fields import MoneyField

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    ticket = models.OneToOneField('events.Ticket', on_delete=models.CASCADE, related_name='payment')
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', default=0)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(blank=True, null=True)