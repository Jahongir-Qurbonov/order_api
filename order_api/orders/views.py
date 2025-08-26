from typing import cast

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from order_api.users.models import User
from order_api.users.models import UserRoles

from .models import Order
from .models import OrderStatus
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)

        match cast("User", request.user).role:
            case UserRoles.CLIENT:
                pass
            case _ if request.method not in SAFE_METHODS:
                raise PermissionDenied

    def get_queryset(self):
        queryset = super().get_queryset()

        match cast("User", self.request.user).role:
            case UserRoles.ADMIN:
                return queryset
            case UserRoles.CLIENT:
                return queryset.filter(owner=self.request.user)
            case UserRoles.WORKER:
                return queryset.filter(
                    Q(worker=self.request.user) | Q(worker__isnull=True),
                )
            case _:
                raise PermissionDenied

    @action(detail=True, methods=["post"], serializer_class=None)
    def receive(self, request: Request, pk=None):
        order = cast("Order", self.get_object())

        if order.status != OrderStatus.CREATED:
            msg = "Only created orders can be received."
            raise PermissionDenied(msg)

        if order.worker is not None:
            msg = "This order has already been assigned to a worker."
            raise PermissionDenied(msg)

        order.worker = request.user
        order.status = OrderStatus.RECEIVED
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)
