import logging

logger = logging.getLogger(__name__)


def send_tenant_signup_notification(tenant, user):
    """Placeholder for tenant signup notification email."""
    logger.info(
        'EMAIL PLACEHOLDER: New tenant signup — %s (%s) — contact: %s <%s>',
        tenant.company_name,
        tenant.tenant_code,
        tenant.contact_person,
        user.email,
    )


def send_tenant_approved_notification(tenant):
    """Placeholder for tenant approval notification."""
    logger.info(
        'EMAIL PLACEHOLDER: Tenant approved — %s (%s) — %s',
        tenant.company_name,
        tenant.tenant_code,
        tenant.email_id,
    )
