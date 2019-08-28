"""User authentication and user access models."""

from django.db import models
from soft_delete_it.models import SoftDeleteModel
from rest_framework_jwt.settings import api_settings
import uuid
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class Role(SoftDeleteModel):
    """User access roles and levels."""

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        """Display name by default."""
        return self.name


class UserManager(BaseUserManager):
    """Overide create user methods."""

    def create_user(
        self, email, password=None,
        is_superuser=False,
        is_staff=False, is_active=False
    ):
        """Default create user method."""
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')

        user_obj = self.model(
            email=self.normalize_email(email)
        )

        user_obj.set_password(password)
        user_obj.is_superuser = is_superuser
        user_obj.is_staff = is_staff
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password):
        """Staff user."""
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
        )

        return user

    def create_superuser(self, email, password):
        """Super user."""
        user = self.create_user(
            email=email,
            password=password,
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        return user


class User(AbstractBaseUser, PermissionsMixin, SoftDeleteModel):
    """User data."""

    email = models.EmailField(max_length=30, unique=True)
    username = models.CharField(max_length=15, unique=True, null=False,
                                blank=False)
    password = models.CharField(max_length=1000, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, default=2)
    GUID = models.UUIDField(default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_email(self):
        """User email."""
        return self.email

    def get_username(self):
        """User username."""
        return self.username

    def get_unique_id(self):
        """User UUID."""
        return self.GUID

    @property
    def gen_token(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token

    def __str__(self):
        """Display user email by default."""
        return self.email


class Profile(models.Model):
    """User Profile data."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False,
                                null=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    other_names = models.CharField(max_length=80, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        """Display user's full name by default."""
        return self.first_name + ' ' + self.other_names
