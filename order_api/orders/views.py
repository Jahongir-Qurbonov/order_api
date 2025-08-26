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
from .serializers import CancelOrderSerializer
from .serializers import CompleteOrderSerializer
from .serializers import OrderSerializer
from .serializers import PayOrderSerializer
from .serializers import ReceiveOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)

        match cast("User", request.user).role:
            case UserRoles.CLIENT:
                if request.get_full_path().endswith(
                    "/receive/",
                ) and request.get_full_path().endswith("/complete/"):
                    raise PermissionDenied
            case UserRoles.WORKER:
                if request.method not in SAFE_METHODS and not (
                    request.get_full_path().endswith("/receive/")
                    or request.get_full_path().endswith("/complete/")
                    or request.get_full_path().endswith("/cancel/")
                ):
                    raise PermissionDenied
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
                    Q(worker=self.request.user)
                    | (Q(worker__isnull=True) & Q(status=OrderStatus.CREATED)),
                )
            case _:
                raise PermissionDenied

    @action(detail=True, methods=["post"], serializer_class=ReceiveOrderSerializer)
    def receive(self, request: Request, pk=None):
        order = cast("Order", self.get_object())
        user = cast("User", request.user)

        if user.role != UserRoles.WORKER:
            msg = "Only workers can receive orders."
            raise PermissionDenied(msg)

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

    @action(detail=True, methods=["post"], serializer_class=CompleteOrderSerializer)
    def complete(self, request: Request, pk=None):
        order = cast("Order", self.get_object())
        user = cast("User", request.user)

        if user.role != UserRoles.WORKER:
            msg = "Only workers can complete orders"
            raise PermissionDenied(msg)

        if order.worker != user:
            msg = "You can only complete orders assigned to you"
            raise PermissionDenied(msg)

        if order.status != OrderStatus.RECEIVED:
            msg = "Only received orders can be completed"
            raise PermissionDenied(msg)

        order.status = OrderStatus.COMPLETED
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], serializer_class=PayOrderSerializer)
    def pay(self, request: Request, pk=None):
        serializer = PayOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = cast("Order", self.get_object())
        user = cast("User", request.user)

        if user.role != UserRoles.CLIENT:
            msg = "Only clients can pay for orders"
            raise PermissionDenied(msg)

        if order.owner != user:
            msg = "You can only pay for your own orders"
            raise PermissionDenied(msg)

        if order.status != OrderStatus.COMPLETED:
            msg = "Only completed orders can be paid"
            raise PermissionDenied(msg)

        order.status = OrderStatus.PAID
        order.payment_system = serializer.validated_data["payment_system"]
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], serializer_class=CancelOrderSerializer)
    def cancel(self, request: Request, pk=None):
        order = cast("Order", self.get_object())
        user = cast("User", request.user)

        if user.role == UserRoles.CLIENT:
            if order.owner != user:
                msg = "You can only cancel your own orders"
                raise PermissionDenied(msg)
            if order.status not in [OrderStatus.CREATED, OrderStatus.RECEIVED]:
                msg = "You can only cancel orders that are created or received"
                raise PermissionDenied(msg)
        elif user.role == UserRoles.WORKER:
            if order.worker != user:
                msg = "You can only cancel orders assigned to you"
                raise PermissionDenied(msg)
            if order.status != OrderStatus.RECEIVED:
                msg = "You can only cancel received orders"
                raise PermissionDenied(msg)
        else:
            msg = "Only clients and workers can cancel orders"
            raise PermissionDenied(msg)

        order.status = OrderStatus.CANCELLED
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)
