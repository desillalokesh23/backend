from django.utils import timezone

from master.constants.tenant import ProfileReviewStatus
from master.services.email_service import send_profile_review_notification
from master.utils.profile import check_profile_completion


class TenantService:
    @staticmethod
    def update_profile(tenant, data: dict, user=None):
        if tenant.is_profile_locked:
            raise ValueError('Profile is locked while under super admin review.')

        file_fields = [
            'company_logo',
            'profile_picture',
            'gst_document',
            'pan_document',
            'bank_document',
            'office_document',
        ]
        readonly_keys = {
            'id',
            'tenant_code',
            'status',
            'created_at',
            'profile_review_status',
            'profile_submitted_at',
        }
        for key, value in data.items():
            if key in readonly_keys:
                continue
            if key in file_fields:
                if value is not None:
                    setattr(tenant, key, value)
            elif hasattr(tenant, key):
                setattr(tenant, key, value)
        if user and hasattr(tenant, 'updated_by'):
            tenant.updated_by = user
        tenant.save()
        check_profile_completion(tenant)
        return tenant

    @staticmethod
    def submit_profile_for_review(tenant):
        if tenant.is_profile_locked:
            raise ValueError('Profile has already been submitted for review.')

        completed, missing = check_profile_completion(tenant)
        if not completed:
            raise ValueError(f'Complete required fields before submitting: {", ".join(missing)}')

        tenant.profile_review_status = ProfileReviewStatus.SUBMITTED
        tenant.profile_submitted_at = timezone.now()
        tenant.save(
            update_fields=['profile_review_status', 'profile_submitted_at', 'updated_at']
        )
        send_profile_review_notification(tenant)
        return tenant
