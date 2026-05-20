from rest_framework import serializers

from master.models.masters import (
    Branch,
    Driver,
    PackageType,
    RouteMaster,
    ServiceType,
    VehicleType,
    Warehouse,
)


class BranchSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.display_name', read_only=True)

    class Meta:
        model = Branch
        fields = [
            'id',
            'name',
            'code',
            'address',
            'city',
            'state',
            'pincode',
            'phone',
            'gps_lat',
            'gps_lng',
            'manager',
            'manager_name',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'manager_name']


class WarehouseSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'name',
            'code',
            'branch',
            'branch_name',
            'address',
            'capacity_sqft',
            'contact_person',
            'phone',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'branch_name']


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteMaster
        fields = [
            'id',
            'source',
            'destination',
            'distance_km',
            'estimated_time_minutes',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ['id', 'name', 'code', 'max_weight_kg', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name', 'code', 'capacity_kg', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class DriverSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Driver
        fields = [
            'id',
            'full_name',
            'phone',
            'license_number',
            'license_expiry',
            'email',
            'branch',
            'branch_name',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'branch_name']
