from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

def send_registration_email(user : CustomUser):
    subject = "Successful Registration to Foodify"
    message = f"""
    Dear {user.username.capitalize()},

    Thank you for registering to Foodify. We hope your expectations will be met by our five star services.

    Best regards,
    Foodify team
    """

    send_mail(
        subject,message,settings.EMAIL_HOST_USER, recipient_list = [user.email]
    )