"""
Test for the contract API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Contract,
    Customer
)

from customer.serializers import ContractSerializer

from random import randint

from datetime import date


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)

def create_customer(user, **params):
    """Create and return a sample customer."""
    defaults = {
        'name': 'Sample Customer Name',
    }
    defaults.update(params)

    customer = Customer.objects.create(user=user, **defaults)
    return customer

def detail_url(customer_id):
    """Create and return an customer contracts URL."""
    return reverse('customer:customer-contract-list', args=[customer_id])


class PrivateContractsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.customer = create_customer(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_contracts_limited_to_customer(self):
        """Test list of contracts is liimited to customer."""
        today = date.today()
        customer2 = create_customer(name='Sample Customer 2',user=self.user)
        Contract.objects.create(user=self.user, title='Sample title for customer 2', initial_date=today, balance=randint(0,1000),customer=customer2)
        contract = Contract.objects.create(user=self.user, title='Sample title 1', initial_date=today, balance=randint(0,1000),customer=self.customer)

        url = detail_url(self.customer.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], contract.title)
        self.assertEqual(res.data[0]['id'], contract.id)
