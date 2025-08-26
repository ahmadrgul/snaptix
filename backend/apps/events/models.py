import uuid
from django.db import models
from apps.users.models import Organizer
from djmoney.models.fields import MoneyField

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('concert', 'Concert'),
        ('conference', 'Conference'),  
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('festival', 'Festival'),
        ('meetup', 'Meetup'),
        ('sports', 'Sports'),
        ('theater', 'Theater'),
        ('exhibition', 'Exhibition'),
        ('other', 'Other')
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='other')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    booking_deadline = models.DateTimeField()
    venue_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    sold_tickets = models.PositiveIntegerField(default=0)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    is_free = models.BooleanField(default=False)
    is_listed = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
        ('checked_in', 'Checked In'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    attendee_name = models.CharField(max_length=255)
    attendee_email = models.EmailField()
    # payment field will be added later
    # payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='booking', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
