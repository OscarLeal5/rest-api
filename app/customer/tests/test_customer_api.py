"""
Tests for Customer API.
"""
from http.cookiejar import DefaultCookiePolicy
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from customer import serializers

from core.models import Customer

from customer.serializers import (
    CustomerSerializer,
    CustomerDetailSerializer,
)


CUSTOMERS_URL = reverse('customer:customer-list')

def detail_url(customer_id):
    """Create and return a customer detail URL."""
    return reverse('customer:customer-detail', args=[customer_id])


def create_customer(user, **params):
    """Create and return a sample customer."""
    defaults = {
        'name': 'Sample Customer Name',
    }
    defaults.update(params)

    customer = Customer.objects.create(user=user, **defaults)
    return customer

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicCustomerAPITests(TestCase):
    """Test unautheticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CUSTOMERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCustomerAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrive_customers(self):
        """Test retriving a list of customers."""
        create_customer(user=self.user)
        create_customer(user=self.user)

        res = self.client.get(CUSTOMERS_URL)

        customers = Customer.objects.all().order_by('-id')
        serializer = CustomerSerializer(customers, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_customer_list_limited_to_user(self):
        """Test list of customers limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='password123')

        create_customer(user=other_user)
        create_customer(user=self.user)

        res = self.client.get(CUSTOMERS_URL)

        customers = Customer.objects.filter(user=self.user)
        serializer = CustomerSerializer(customers, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_customer_detail(self):
        """Test customer detail."""
        customer = create_customer(user=self.user)

        url = detail_url(customer.id)
        res = self.client.get(url)

        serializer = CustomerDetailSerializer(customer)
        self.assertEqual(res.data, serializer.data)

    def test_create_customer(self):
        """Test creating a customer."""
        payload = {
            'name': 'Sample Customer'
        }
        res = self.client.post(CUSTOMERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(customer, k), v)
        self.assertEqual(customer.user, self.user)

    def test_partial_update(self):
        """Test partial update of a customer."""
        original_name = 'Original Name'
        customer = create_customer(
            user=self.user,
            name=original_name,
        )

        payload = {'name': 'New Customer Name'}
        url = detail_url(customer.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.name, payload['name'])
        self.assertEqual(customer.user, self.user)

    def test_full_update(self):
        """Test full update of customer."""
        customer = create_customer(
            user=self.user,
            name='Sample Customer Name'
        )

        payload = {
            'name': 'New Sample Customer Name'
        }
        url = detail_url(customer.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(customer, k), v)
        self.assertEqual(customer.user, self.user)

    def test_update_user_return_error(self):
        """Test changing the customer user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        customer = create_customer(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(customer.id)
        self.client.patch(url, payload)

        customer.refresh_from_db()
        self.assertEqual(customer.user, self.user)

    def test_delete_customer(self):
        """Test deleting a customer successful."""
        customer = create_customer(user=self.user)

        url = detail_url(customer.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=customer.id).exists())

    def test_customer_others_users_customer_error(self):
        """Test trying to delete another user customer gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        customer = create_customer(user=new_user)

        url = detail_url(customer.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Customer.objects.filter(id=customer.id).exists())
