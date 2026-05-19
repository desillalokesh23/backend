from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from master.constants.modules import TenantModule
from master.models.rbac import Role, SystemPermission
from master.models.user import User
from master.permissions.base import IsAuthenticatedTenantUser, IsTenantAdmin
from master.permissions.rbac import HasModulePermission
from master.serializers.rbac import (
    RolePermissionMatrixSerializer,
    RoleSerializer,
    SystemPermissionSerializer,
    TenantUserSerializer,
)
from master.views.base import TenantScopedViewSet


class RoleViewSet(TenantScopedViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [IsAuthenticatedTenantUser(), HasModulePermission()]

    @action(detail=True, methods=['get', 'put'], url_path='permissions')
    def permissions(self, request, pk=None):
        role = self.get_object()
        if request.method == 'GET':
            serializer = RolePermissionMatrixSerializer(role)
            return Response(serializer.data)
        perm_map = request.data.get('permissions', {})
        if isinstance(perm_map, list):
            perm_map = {item['codename']: item.get('granted', False) for item in perm_map}
        sync_data = {k: bool(v) for k, v in perm_map.items()}
        from master.services.permission_service import sync_role_permissions

        sync_role_permissions(role, sync_data)
        return Response(RolePermissionMatrixSerializer(role).data)


class TenantUserViewSet(TenantScopedViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = TenantUserSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [IsAuthenticatedTenantUser(), IsTenantAdmin()]

    def get_queryset(self):
        return User.objects.filter(tenant=self.request.user.tenant).select_related(
            'role', 'branch'
        )

    def perform_destroy(self, instance):
        instance.is_active_user = False
        instance.is_active = False
        instance.save(update_fields=['is_active_user', 'is_active'])


class SystemPermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SystemPermission.objects.all()
    serializer_class = SystemPermissionSerializer
    permission_classes = [IsAuthenticatedTenantUser]
