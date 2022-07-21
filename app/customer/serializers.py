"""
Serializers for Customer API's.
"""
from rest_framework import serializers

from core.models import (
    Customer,
    Contract,
    Service,
)


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Services."""

    class Meta:
        model = Service
        fields = ['id','title','price']
        read_only_fields = ['id']


class ServiceDetailSerializer(ServiceSerializer):
    """Serializer for contract detail view."""

    class Meta(ServiceSerializer.Meta):
        fields = ServiceSerializer.Meta.fields


class ContractSerializer(serializers.ModelSerializer):
    """Serializer for Contracts."""

    class Meta:
        model = Contract
        fields = ['id','title','initial_date','balance','customer','payment_option']
        read_only_fields = ['id']


class ContractDetailSerializer(ContractSerializer):
    """Serializer for contract detail view."""

    class Meta(ContractSerializer.Meta):
        fields = ContractSerializer.Meta.fields


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customers."""

    class Meta:
        model = Customer
        fields = ['id','name']
        read_only_fields = ['id']


class CustomerDetailSerializer(CustomerSerializer):
    """Serializer for customer detail view."""

    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields
