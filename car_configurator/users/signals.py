# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Only save profile if it exists
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # You could create it here if necessary
        Profile.objects.create(user=instance)