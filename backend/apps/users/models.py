from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    """
    Custom user model that will store only the required fields,
    it will be extended using profile models for differet user types.
    """
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(unique=True)
    USER_ROLE_CHOICES = {
        "admin": "Admin",
        "organizer": "Organizer",
        # can be extended with more roles
    }
    role = models.CharField(default='organizer', choices=USER_ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Organizer(CustomUser):
    """
    Organizer model extends the CustomUser model,
    it includes a phone number field but can be extended in future.
    """
    phone = PhoneNumberField(unique=True)