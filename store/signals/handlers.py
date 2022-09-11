from ..models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from . import order_created

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])


@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])

# FOR WHERE I WILL FIRE THE SIGNALS
# order_created.send(sender='', order='')
# sender can be anything, ex: 'instance of a class' or 'any string'

