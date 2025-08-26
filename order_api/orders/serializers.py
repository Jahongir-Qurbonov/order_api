from rest_framework import serializers

from order_api.users.api.serializers import UserSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    worker = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "owner",
            "worker",
            "description",
            "status",
            "price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "worker",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class ReceiveOrderSerializer(serializers.Serializer):
    pass


class CompleteOrderSerializer(serializers.Serializer):
    pass


class PayOrderSerializer(serializers.Serializer):
    pass


class CancelOrderSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=255, required=False)
