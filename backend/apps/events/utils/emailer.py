from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage

def send_ticket_email(qr_bytes, ticket):
    subject = f"Booking Confirmed: {ticket.event.title} — See You There!"
    html_content = render_to_string("emails/ticket_email.html", {
        "ticket": ticket,
        "event": ticket.event,
        "company_name": "Snaptix",
        "support_email": "support@snaptix.com",
        "support_phone": "+1-800-123-4567",
    })

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        to=[ticket.attendee_email]
    )
    email.attach_alternative(html_content, "text/html")

    qr_img = MIMEImage(qr_bytes)
    qr_img.add_header("Content-ID", "<ticket_qr>")
    qr_img.add_header("Content-Disposition", "inline", filename="ticket.png")
    email.attach(qr_img)

    email.send()