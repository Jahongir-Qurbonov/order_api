from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Order
        fields = [
            "owner",
            "worker",
            "description",
            "status",
            "price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "worker",
            "status",
            "created_at",
            "updated_at",
        ]
