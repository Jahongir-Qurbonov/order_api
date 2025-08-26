from django.db import models


class OrderStatus(models.TextChoices):
    CREATED = "created", "Created"
    RECEIVED = "received", "Received"


class Order(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    worker = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
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
