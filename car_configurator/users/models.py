# users/models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ContactForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact form from {self.name} ({self.email})"