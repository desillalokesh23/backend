from django.http import JsonResponse

from master.constants.modules import PENDING_TENANT_ALLOWED_MODULES, TenantModule
from master.constants.tenant import TenantStatus

# API path prefixes mapped to modules for restriction checks
MODULE_PATH_MAP = {
    '/api/v1/operations': TenantModule.OPERATIONS,
    '/api/v1/fleet': TenantModule.FLEET,
    '/api/v1/reports': TenantModule.REPORTS,
    '/api/v1/marketplace': TenantModule.MARKETPLACE,
    '/api/v1/accounts': TenantModule.ACCOUNTS,
}


class TenantRestrictionMiddleware:
    """
    Blocks API access to restricted modules for pending/unapproved tenants.
    Profile and all masters endpoints remain accessible regardless of profile completion.
    """

    EXEMPT_PREFIXES = (
        '/api/v1/auth/',
        '/api/v1/profile/',
        '/api/v1/masters/',
        '/admin/',
        '/api/schema/',
        '/api/docs/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if any(path.startswith(p) for p in self.EXEMPT_PREFIXES):
            return self.get_response(request)

        if not path.startswith('/api/v1/'):
            return self.get_response(request)

        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return self.get_response(request)

        if getattr(user, 'is_super_admin', False) or user.is_superuser:
            return self.get_response(request)

        tenant = getattr(user, 'tenant', None)
        if not tenant:
            return self.get_response(request)

        module = self._resolve_module(path)
        if not module:
            return self.get_response(request)

        if tenant.status == TenantStatus.FROZEN:
            return JsonResponse(
                {'detail': 'Tenant account is frozen. Contact support.'},
                status=403,
            )

        if tenant.status == TenantStatus.PENDING:
            if module not in PENDING_TENANT_ALLOWED_MODULES:
                return JsonResponse(
                    {
                        'detail': 'Tenant pending approval. Only profile and masters are accessible.',
                        'code': 'tenant_pending',
                    },
                    status=403,
                )

        return self.get_response(request)

    def _resolve_module(self, path: str) -> str | None:
        if path.startswith('/api/v1/profile'):
            return TenantModule.PROFILE
        for prefix, module in MODULE_PATH_MAP.items():
            if path.startswith(prefix):
                return module
        return None
