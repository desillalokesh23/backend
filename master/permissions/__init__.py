from master.permissions.base import IsAuthenticatedTenantUser, IsTenantAdmin
from master.permissions.rbac import HasModulePermission

__all__ = ['IsAuthenticatedTenantUser', 'IsTenantAdmin', 'HasModulePermission']
