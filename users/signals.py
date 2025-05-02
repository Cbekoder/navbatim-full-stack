from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, BusinessProfile, ClientProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'business':
            BusinessProfile.objects.create(user=instance)
        else:
            ClientProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'business':
        if hasattr(instance, 'business_profile'):
            instance.business_profile.save()
        else:
            BusinessProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'client_profile'):
            instance.client_profile.save()
        else:
            ClientProfile.objects.create(user=instance)
