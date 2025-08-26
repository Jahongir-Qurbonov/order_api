from rest_framework import serializers

from order_api.users.models import RegistrationRoles
from order_api.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "email", "url"]
        read_only_fields = ["email"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserRegistrationSerializer(serializers.ModelSerializer[User]):
    role = serializers.ChoiceField(choices=RegistrationRoles.choices)

    class Meta:
        model = User
        fields = ["name", "email", "role", "password"]

        extra_kwargs = {
            "password": {"write_only": True},
        }
