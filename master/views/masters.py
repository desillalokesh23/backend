from master.constants.modules import TenantModule
from master.models.masters import (
    Branch,
    Driver,
    PackageType,
    RouteMaster,
    ServiceType,
    VehicleType,
    Warehouse,
)
from master.permissions.rbac import HasModulePermission
from master.serializers.masters import (
    BranchSerializer,
    DriverSerializer,
    PackageTypeSerializer,
    RouteSerializer,
    ServiceTypeSerializer,
    VehicleTypeSerializer,
    WarehouseSerializer,
)
from master.views.base import TenantScopedViewSet


class BranchViewSet(TenantScopedViewSet):
    queryset = Branch.objects.select_related('manager')
    serializer_class = BranchSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [*super().get_permissions(), HasModulePermission()]


class WarehouseViewSet(TenantScopedViewSet):
    queryset = Warehouse.objects.select_related('branch')
    serializer_class = WarehouseSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [*super().get_permissions(), HasModulePermission()]


class RouteViewSet(TenantScopedViewSet):
    queryset = RouteMaster.objects.all()
    serializer_class = RouteSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [*super().get_permissions(), HasModulePermission()]


class ServiceTypeViewSet(TenantScopedViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [*super().get_permissions(), HasModulePermission()]


class PackageTypeViewSet(TenantScopedViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [*super().get_permissions(), HasModulePermission()]


class VehicleTypeViewSet(TenantScopedViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [*super().get_permissions(), HasModulePermission()]


class DriverViewSet(TenantScopedViewSet):
    queryset = Driver.objects.select_related('branch')
    serializer_class = DriverSerializer
    required_module = TenantModule.MASTERS

    def get_permissions(self):
        return [*super().get_permissions(), HasModulePermission()]
