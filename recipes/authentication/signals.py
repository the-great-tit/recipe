"""Signals for user actions."""

from .models import User, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile on saving the user."""
    if created:  # noqa
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Create user profile on saving the user."""
    instance.profile.save()
