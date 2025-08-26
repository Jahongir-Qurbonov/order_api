from decimal import Decimal

from django.db import models

from order_api.users.models import User


class Account(models.Model):  # noqa: DJ008
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="account",
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )


class Transaction(models.Model):  # noqa: DJ008
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
