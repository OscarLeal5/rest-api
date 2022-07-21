"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Customer(models.Model):
    """Customer object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Service(models.Model):
    """Service object."""
    def get_unknown_contract():
        return Contract.objects.get_or_create(name='Unknown Contract')[0]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class Contract(models.Model):
    """Contract object."""
    def get_unknown_customer():
        return Customer.objects.get_or_create(name='Unknown Customer')[0]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    initial_date = models.DateField(null=True, blank=True)
    balance = models.IntegerField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET(get_unknown_customer))
    services = models.ManyToManyField(Service, blank=True, null=True)

    ONE = 1
    TWO = 2
    THREE = 3
    PAYMENT_CHOICES = [
        (ONE, 'One'),
        (TWO, 'Two'),
        (THREE, 'Three'),
    ]
    payment_option = models.IntegerField(choices=PAYMENT_CHOICES, default=ONE)

    def __str__(self):
        return self.title
