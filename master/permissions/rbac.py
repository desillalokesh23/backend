from rest_framework.permissions import BasePermission

from master.constants.tenant import ProfileReviewStatus
from master.models.rbac import RolePermission


class HasModulePermission(BasePermission):
    """
    View should define: required_module, required_action (default: view).
    Super admins and tenant admins bypass checks.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or getattr(user, 'is_super_admin', False):
            return True
        if getattr(user, 'is_tenant_admin', False):
            # Tenant admins can always list/view masters, but cannot create/update/delete
            # until profile is completed AND approved by super admin.
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            tenant = getattr(user, 'tenant', None)
            if tenant and getattr(tenant, 'profile_completed', False) and getattr(tenant, 'profile_review_status', None) == ProfileReviewStatus.APPROVED:
                return True
            return False

        module = getattr(view, 'required_module', None)
        action = getattr(view, 'required_action', 'view')
        if not module:
            return True

        role = getattr(user, 'role', None)
        if not role or not role.is_active:
            return False

        codename = f'{module}.{action}'
        return RolePermission.objects.filter(
            role=role,
            permission__codename=codename,
            granted=True,
        ).exists()
