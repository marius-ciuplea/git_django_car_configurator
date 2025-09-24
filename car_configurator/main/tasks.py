from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_offer_email(user_email):
    
    send_mail(subject="We received your car configuration.",
               message="Thank you for sending your car configuration! We'll get in touch you soon.",
               from_email=settings.DEFAULT_FROM_EMAIL,
               recipient_list=[user_email],
               fail_silently=False,
               )