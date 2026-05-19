from master.constants.modules import MODULE_ACTIONS, MODULES
from master.models.rbac import RolePermission, SystemPermission


def seed_system_permissions():
    created = 0
    for module_key, module_label in MODULES:
        for action in MODULE_ACTIONS:
            codename = f'{module_key}.{action}'
            label = f'{module_label} — {action.title()}'
            _, was_created = SystemPermission.objects.get_or_create(
                codename=codename,
                defaults={
                    'module': module_key,
                    'action': action,
                    'label': label,
                },
            )
            if was_created:
                created += 1
    return created


def sync_role_permissions(role, permission_map: dict[str, bool]):
    """
    permission_map: { codename: granted }
    """
    permissions = SystemPermission.objects.filter(codename__in=permission_map.keys())
    for perm in permissions:
        RolePermission.objects.update_or_create(
            role=role,
            permission=perm,
            defaults={'granted': permission_map.get(perm.codename, False)},
        )


def get_role_permission_matrix(role):
    all_perms = SystemPermission.objects.all().order_by('module', 'action')
    granted = set(
        RolePermission.objects.filter(role=role, granted=True).values_list(
            'permission__codename', flat=True
        )
    )
    matrix = []
    for perm in all_perms:
        matrix.append(
            {
                'id': perm.id,
                'module': perm.module,
                'action': perm.action,
                'codename': perm.codename,
                'label': perm.label,
                'granted': perm.codename in granted,
            }
        )
    return matrix
