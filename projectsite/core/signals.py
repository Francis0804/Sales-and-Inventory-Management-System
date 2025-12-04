# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserRole


@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    """Auto-create UserRole when a new User is created"""
    if created:
        UserRole.objects.get_or_create(
            user=instance,
            defaults={'role': 'cashier'}  # Default to Cashier role
        )


@receiver(post_save, sender=User)
def save_user_role(sender, instance, **kwargs):
    """Save UserRole when User is saved"""
    try:
        instance.user_role.save()
    except UserRole.DoesNotExist:
        UserRole.objects.create(user=instance, role='cashier')
