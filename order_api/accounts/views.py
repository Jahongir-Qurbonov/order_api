from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .models import Transaction
from .serializers import AccountSerializer
from .serializers import TransactionSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(account__user=self.request.user)
