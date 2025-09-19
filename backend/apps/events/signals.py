from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from apps.events.utils.qr_generater import generate_qr
from apps.events.utils.emailer import send_ticket_email

@receiver(post_save, sender=Ticket)
def ticket_paid_handler(sender, instance, created, **kwargs):
    if not created and instance.status == "paid":
        qr = generate_qr(f"http://localhost:5173/tickets/{instance.pk}")
        send_ticket_email(qr, instance)
