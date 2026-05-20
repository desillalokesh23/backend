from django.conf import settings
from django.db import models

from master.models.base import BaseModel


class Branch(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    gps_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    gps_lng = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branches',
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_branch'
        unique_together = [('tenant', 'name')]
        ordering = ['name']


class Warehouse(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='warehouses')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='warehouses')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    capacity_sqft = models.PositiveIntegerField(null=True, blank=True)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_warehouse'
        ordering = ['name']


class RouteMaster(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='routes')
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_time_minutes = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_route'
        ordering = ['source', 'destination']


class ServiceType(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='service_types')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_service_type'
        unique_together = [('tenant', 'name')]


class PackageType(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='package_types')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True)
    max_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_package_type'
        unique_together = [('tenant', 'name')]


class VehicleType(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='vehicle_types')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True)
    capacity_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_vehicle_type'
        unique_together = [('tenant', 'name')]


class Driver(BaseModel):
    tenant = models.ForeignKey('master.Tenant', on_delete=models.CASCADE, related_name='drivers')
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='drivers',
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50, blank=True)
    license_expiry = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_driver'
        ordering = ['full_name']
