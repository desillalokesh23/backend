class TenantModule:
    OPERATIONS = 'operations'
    FLEET = 'fleet'
    REPORTS = 'reports'
    MARKETPLACE = 'marketplace'
    ACCOUNTS = 'accounts'
    MASTERS = 'masters'
    PROFILE = 'profile'


MODULES = [
    (TenantModule.OPERATIONS, 'Operations'),
    (TenantModule.FLEET, 'Fleet'),
    (TenantModule.REPORTS, 'Reports'),
    (TenantModule.MARKETPLACE, 'Marketplace'),
    (TenantModule.ACCOUNTS, 'Accounts'),
    (TenantModule.MASTERS, 'Masters'),
    (TenantModule.PROFILE, 'Profile'),
]

MODULE_ACTIONS = ['view', 'create', 'edit', 'delete', 'export']

# Modules accessible before tenant approval (masters API exempted in middleware)
PENDING_TENANT_ALLOWED_MODULES = {TenantModule.MASTERS, TenantModule.PROFILE}
