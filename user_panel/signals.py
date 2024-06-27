from django.db.models.signals import Signal, post_save
from django.dispatch import receiver
from .models import Order_confirm
from admin_panel.models import Notification
from django.contrib.auth.models import User

order_confirmed = Signal(providing_args=["order"])

@receiver(post_save, sender=Order_confirm)
def order_confirmation_handler(sender, instance, **kwargs):
    if instance.status == 'Confirmed':
        admin = User.objects.get(username='admin_username')  # Replace with the admin's username
        message = f"New order placed with ID #{instance.id}"
        notification = Notification.objects.create(user=admin, message=message)
        order_confirmed.send(sender=sender, order=instance)
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserLoginLog  # Import your UserLoginLog model

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Create a UserLoginLog entry when a user logs in
    UserLoginLog.objects.create(user=user)
