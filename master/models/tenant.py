from django.db import models
from django.utils import timezone

from master.constants.tenant import TenantStatus
from master.models.base import BaseModel
from master.utils.tenant_code import generate_tenant_code


def tenant_upload_path(instance, filename):
    return f'tenants/{instance.id}/{filename}'


class Tenant(BaseModel):
    tenant_code = models.CharField(max_length=32, unique=True, editable=False)
    company_name = models.CharField(max_length=255)
    company_full_address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100, blank=True)
    gstin_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    account_holder_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    subscription_start = models.DateField(null=True, blank=True)
    subscription_end = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TenantStatus.CHOICES,
        default=TenantStatus.PENDING,
        db_index=True,
    )
    company_logo = models.ImageField(upload_to=tenant_upload_path, null=True, blank=True)
    gst_document = models.FileField(upload_to=tenant_upload_path, null=True, blank=True)
    pan_document = models.FileField(upload_to=tenant_upload_path, null=True, blank=True)
    bank_document = models.FileField(upload_to=tenant_upload_path, null=True, blank=True)
    office_document = models.FileField(upload_to=tenant_upload_path, null=True, blank=True)
    home_branch_gps_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    home_branch_gps_lng = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    profile_completed = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'master_tenant'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tenant_code} — {self.company_name}'

    def save(self, *args, **kwargs):
        if not self.tenant_code:
            self.tenant_code = generate_tenant_code()
        super().save(*args, **kwargs)

    @property
    def is_approved(self):
        return self.status in (TenantStatus.APPROVED, TenantStatus.ACTIVE)

    def mark_approved(self):
        self.status = TenantStatus.APPROVED
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_at', 'updated_at'])
