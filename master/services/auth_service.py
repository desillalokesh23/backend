from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q
import logging

from master.constants.modules import MODULE_ACTIONS, MODULES
from master.constants.tenant import TenantStatus
from master.models.rbac import Role
from master.models.tenant import Tenant
from master.models.user import User
from master.services.email_service import send_tenant_signup_notification
from master.services.permission_service import seed_system_permissions, sync_role_permissions
from master.validators.auth import validate_signup_password

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    @transaction.atomic
    def register_tenant(*, email_id, password, company_name, contact_person, phone_number):
        validate_signup_password(password)
        email = email_id.lower().strip()

        if Tenant.objects.filter(email_id=email).exists():
            logger.warning(f"Signup attempt with existing email: {email}")
            raise ValueError('A tenant with this email already exists.')
        if User.objects.filter(email=email).exists():
            logger.warning(f"Signup attempt with existing user email: {email}")
            raise ValueError('A user with this email already exists.')

        tenant = Tenant.objects.create(
            company_name=company_name.strip(),
            contact_person=contact_person.strip(),
            email_id=email,
            phone_number=phone_number.strip(),
            status=TenantStatus.PENDING,
        )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=contact_person.split()[0] if contact_person else '',
            last_name=' '.join(contact_person.split()[1:]) if contact_person else '',
            tenant=tenant,
            phone_number=phone_number.strip(),
            is_tenant_admin=True,
            is_active=True,
            is_active_user=True,
        )

        seed_system_permissions()
        admin_role = Role.objects.create(
            tenant=tenant,
            name='Tenant Admin',
            description='Default administrator role with full masters access',
            created_by=user,
        )
        all_codenames = {f'{m[0]}.{a}': True for m in MODULES for a in MODULE_ACTIONS}
        sync_role_permissions(admin_role, all_codenames)
        user.role = admin_role
        user.save(update_fields=['role'])

        logger.info(f"New tenant registered: {tenant.tenant_code} - {tenant.company_name}")
        send_tenant_signup_notification(tenant, user)
        return tenant, user

    @staticmethod
    def authenticate_user(email: str, password: str):
        login = email.lower().strip()
        user = (
            User.objects.filter(Q(email__iexact=login) | Q(username__iexact=login))
            .select_related('tenant', 'role')
            .first()
        )
        if not user or not user.check_password(password):
            logger.warning(f"Failed login attempt for email: {email}")
            return None
        if not user.is_active or not user.is_active_user:
            logger.warning(f"Inactive user login attempt: {email}")
            return None
        if user.tenant and user.tenant.status == TenantStatus.FROZEN:
            logger.warning(f"Frozen tenant login attempt: {email}")
            return None

        logger.info(f"Successful login: {user.email} (tenant: {user.tenant.tenant_code if user.tenant else 'None'})")
        return user
