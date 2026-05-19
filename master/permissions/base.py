from rest_framework.permissions import BasePermission


class IsAuthenticatedTenantUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'tenant_id', None))


class IsTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (getattr(user, 'is_tenant_admin', False) or user.is_superuser)
        )
