"""
Views for the customer APIs.
"""
from tokenize import Token
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework. permissions import IsAuthenticated
from rest_framework.decorators import action

from core.models import (
    Customer,
    Contract,
    Service,
)
from customer import serializers


class CustomerViewSet(viewsets.ModelViewSet):
    """View for manage customer APIs."""
    serializer_class = serializers.CustomerDetailSerializer
    queryset = Customer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive customers for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.CustomerSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new customer."""
        serializer.save(user=self.request.user)

class ContractViewSet(viewsets.ModelViewSet):
    """Manage contracts in the database."""
    serializer_class = serializers.ContractSerializer
    queryset = Contract.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive contracts for authenticated user."""
        customer = self.kwargs['customer_pk']
        return self.queryset.filter(customer=customer).order_by('-id')

    def perform_create(self, serializer):
        """Create a new contract for customer."""
        customer = self.kwargs['customer_pk']
        serializer.save(customer=customer)

class ServiceViewSet(viewsets.ModelViewSet):
    """Manage services in the database."""
    serializer_class = serializers.ServiceSerializer
    queryset = Service.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive contracts for authenticated user."""
        contract = self.kwargs['contract_pk']
        return self.queryset.filter(contract=contract).order_by('-id')
