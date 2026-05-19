from rest_framework import serializers

from master.models.tenant import Tenant


class TenantProfileSerializer(serializers.ModelSerializer):
    tenant_id = serializers.CharField(source='tenant_code', read_only=True)
    tenant_status = serializers.CharField(source='status', read_only=True)

    class Meta:
        model = Tenant
        fields = [
            'id',
            'tenant_id',
            'company_name',
            'company_full_address',
            'contact_person',
            'email_id',
            'phone_number',
            'country',
            'gstin_number',
            'bank_name',
            'account_holder_name',
            'account_number',
            'ifsc_code',
            'subscription_start',
            'subscription_end',
            'tenant_status',
            'created_at',
            'company_logo',
            'gst_document',
            'pan_document',
            'bank_document',
            'office_document',
            'home_branch_gps_lat',
            'home_branch_gps_lng',
            'profile_completed',
        ]
        read_only_fields = [
            'id',
            'tenant_id',
            'email_id',
            'subscription_start',
            'subscription_end',
            'tenant_status',
            'created_at',
            'profile_completed',
        ]
