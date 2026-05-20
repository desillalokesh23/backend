import random
import string

from django.apps import apps


def generate_tenant_code():
    Tenant = apps.get_model('master', 'Tenant')
    prefix = 'GT'
    while True:
        suffix = ''.join(random.choices(string.digits, k=6))
        code = f'{prefix}{suffix}'
        if not Tenant.objects.filter(tenant_code=code).exists():
            return code
