from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    if created:
        # Notify all workers about new order
        async_to_sync(channel_layer.group_send)(
            "workers",
            {
                "type": "new_order",
                "order_id": instance.id,
                "message": f"New order #{instance.id} created: {instance.description}",
            },
        )
    else:
        # Notify the client about status update
        status_display = instance.get_status_display()
        async_to_sync(channel_layer.group_send)(
            f"client_{instance.owner.id}",
            {
                "type": "order_status_update",
                "order_id": instance.id,
                "status": instance.status,
                "message": f"Order #{instance.id} status updated to {status_display}",
            },
        )
