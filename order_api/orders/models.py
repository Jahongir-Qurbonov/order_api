from django.db import models

from order_api.users.models import User


class OrderStatus(models.TextChoices):
    CREATED = "created", "Created"
    RECEIVED = "received", "Received"


class Order(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    worker = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="assigned_orders",
    )

    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.pk} - {self.status}"
