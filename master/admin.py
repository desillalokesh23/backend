from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from master.constants.tenant import TenantStatus
from master.models.masters import Branch, Driver, PackageType, RouteMaster, ServiceType, VehicleType, Warehouse
from master.models.rbac import Role, RolePermission, SystemPermission
from master.models.tenant import Tenant
from master.models.user import User
from master.services.email_service import send_tenant_approved_notification


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        'tenant_code',
        'company_name',
        'email_id',
        'status',
        'profile_completed',
<<<<<<< HEAD
        'profile_review_status',
        'profile_submitted_at',
=======
>>>>>>> 9909f3cf74a537c9b94dc4a66767f0080f0f36b8
        'subscription_start',
        'subscription_end',
        'created_at',
    )
<<<<<<< HEAD
    list_filter = ('status', 'profile_review_status', 'profile_completed', 'country')
=======
    list_filter = ('status', 'profile_completed', 'country')
>>>>>>> 9909f3cf74a537c9b94dc4a66767f0080f0f36b8
    search_fields = ('tenant_code', 'company_name', 'email_id', 'contact_person')
    readonly_fields = ('tenant_code', 'created_at', 'updated_at', 'approved_at')
    actions = ['approve_tenants', 'activate_tenants', 'freeze_tenants']

    @admin.action(description='Approve selected tenants')
    def approve_tenants(self, request, queryset):
        for tenant in queryset.filter(status=TenantStatus.PENDING):
            tenant.status = TenantStatus.APPROVED
            tenant.save(update_fields=['status', 'updated_at'])
            send_tenant_approved_notification(tenant)

    @admin.action(description='Activate selected tenants')
    def activate_tenants(self, request, queryset):
        queryset.update(status=TenantStatus.ACTIVE)

    @admin.action(description='Freeze selected tenants')
    def freeze_tenants(self, request, queryset):
        queryset.update(status=TenantStatus.FROZEN)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'tenant', 'is_tenant_admin', 'is_active_user', 'is_staff')
    list_filter = ('is_tenant_admin', 'is_active_user', 'tenant')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Tenant', {'fields': ('tenant', 'role', 'branch', 'phone_number', 'is_tenant_admin', 'is_super_admin', 'is_active_user')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Tenant', {'fields': ('tenant', 'role', 'branch', 'phone_number', 'is_tenant_admin')}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('order_id', 'name', 'tenant', 'is_active')
=======
    list_display = ('name', 'tenant', 'is_active')
>>>>>>> 9909f3cf74a537c9b94dc4a66767f0080f0f36b8
    list_filter = ('is_active', 'tenant')
    search_fields = ('name',)


@admin.register(SystemPermission)
class SystemPermissionAdmin(admin.ModelAdmin):
    list_display = ('codename', 'module', 'action', 'label')
    list_filter = ('module', 'action')

    def has_add_permission(self, request):
        return False


admin.site.register(RolePermission)
admin.site.register(Branch)
admin.site.register(Warehouse)
admin.site.register(RouteMaster)
admin.site.register(ServiceType)
admin.site.register(PackageType)
admin.site.register(VehicleType)
admin.site.register(Driver)
