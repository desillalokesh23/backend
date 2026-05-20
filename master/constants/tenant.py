class TenantStatus:
    PENDING = 'pending'
    APPROVED = 'approved'
    ACTIVE = 'active'
    FROZEN = 'frozen'

    CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (ACTIVE, 'Active'),
        (FROZEN, 'Frozen'),
    ]


class ProfileReviewStatus:
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    APPROVED = 'approved'

    CHOICES = [
        (DRAFT, 'Draft'),
        (SUBMITTED, 'Submitted for review'),
        (APPROVED, 'Approved'),
    ]


REQUIRED_PROFILE_FIELDS = [
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
]
