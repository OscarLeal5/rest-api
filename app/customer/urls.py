"""
URL mappinngs for the customer app.
"""
from cgitb import lookup
from django.urls import (
    path,
    include,
)
from rest_framework_nested import routers

from rest_framework.routers import DefaultRouter

from customer import views


customer_router = DefaultRouter()
customer_router.register(r'customers', views.CustomerViewSet, basename='customer')

customer_contract_router = routers.NestedSimpleRouter(customer_router, r'customers', lookup='customer')
customer_contract_router.register(r'contracts', views.ContractViewSet, basename='customer-contract')

contract_service_router = routers.NestedSimpleRouter(customer_contract_router, r'contracts', lookup='contract')
contract_service_router.register(r'services', views.ServiceViewSet, basename='contract-services')

app_name = 'customer'

urlpatterns = [
    path('', include(customer_router.urls)),
    path('', include(customer_contract_router.urls)),
    path('', include(contract_service_router.urls)),
]
