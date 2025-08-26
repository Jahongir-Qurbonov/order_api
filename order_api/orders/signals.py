from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    if not channel_layer:
        return

    if created:
        async_to_sync(channel_layer.group_send)(
            "workers",
            {
                "type": "new_order",
                "order_id": instance.id,
                "message": f"New order #{instance.id} created: {instance.description}",
            },
        )
    else:
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

        if instance.worker:
            worker_msg = f"Order #{instance.id} status updated to {status_display}"
            async_to_sync(channel_layer.group_send)(
                f"worker_{instance.worker.id}",
                {
                    "type": "order_status_update",
                    "order_id": instance.id,
                    "status": instance.status,
                    "message": worker_msg,
                },
            )
