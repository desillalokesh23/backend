import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from master.models.base import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        'master.Tenant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
    )
    role = models.ForeignKey(
        'master.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )
    branch = models.ForeignKey(
        'master.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )
    phone_number = models.CharField(max_length=20, blank=True)
    is_tenant_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    is_active_user = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_user'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email or self.username

    @property
    def display_name(self):
        return self.get_full_name() or self.email
