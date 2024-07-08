from .models import  Profile , Wishlist , Cart ,CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.models import User



@receiver(post_save , sender =CustomUser )
def createCustomerProfile(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user = instance)
        if instance.is_customer :
            Wishlist.objects.create(customer = instance)
            Cart.objects.create(customer = instance)
