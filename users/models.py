from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('business', 'Business'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.email


class BusinessProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='business_covers/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fix: Use the proper import for Category instead of a string
    # This will be a ManyToManyField after we import Category

    def __str__(self):
        return self.business_name


class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
