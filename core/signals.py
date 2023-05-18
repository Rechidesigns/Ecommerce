from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.models import Customer, Seller

User = get_user_model()


@receiver(post_save, sender=User)
def handle_profile_creation(sender, instance, created, **kwargs):
    if created:
        if instance.is_customer is True:
            Customer.objects.create(user=instance)
        else:
            Seller.objects.create(user=instance)


@receiver(post_delete, sender=Customer)
def handle_customer_user_account_deletion(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass


@receiver(post_delete, sender=Seller)
def handle_seller_user_account_deletion(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass
