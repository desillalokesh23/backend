from django.db import models

from master.constants.modules import MODULE_ACTIONS, MODULES
from master.models.base import BaseModel


class SystemPermission(models.Model):
    """Global permission catalog (module + action)."""

    module = models.CharField(max_length=50, choices=MODULES, db_index=True)
    action = models.CharField(max_length=20, choices=[(a, a.title()) for a in MODULE_ACTIONS])
    codename = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=150)

    class Meta:
        db_table = 'master_system_permission'
        unique_together = [('module', 'action')]
        ordering = ['module', 'action']

    def __str__(self):
        return self.label


class Role(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_role'
        unique_together = [('tenant', 'name')]
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.tenant.tenant_code})'


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(
        SystemPermission,
        on_delete=models.CASCADE,
        related_name='role_permissions',
    )
    granted = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_role_permission'
        unique_together = [('role', 'permission')]
