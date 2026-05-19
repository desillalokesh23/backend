from master.utils.profile import check_profile_completion


class TenantService:
    @staticmethod
    def update_profile(tenant, data: dict, user=None):
        file_fields = [
            'company_logo',
            'gst_document',
            'pan_document',
            'bank_document',
            'office_document',
        ]
        for key, value in data.items():
            if key in file_fields:
                if value is not None:
                    setattr(tenant, key, value)
            elif hasattr(tenant, key) and key not in ('id', 'tenant_code', 'status', 'created_at'):
                setattr(tenant, key, value)
        if user:
            tenant.updated_by = user
        tenant.save()
        check_profile_completion(tenant)
        return tenant
