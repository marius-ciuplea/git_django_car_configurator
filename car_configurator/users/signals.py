# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User) #create user profile after a user is registered
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)