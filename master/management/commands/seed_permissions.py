from django.core.management.base import BaseCommand

from master.services.permission_service import seed_system_permissions


class Command(BaseCommand):
    help = 'Seed system permission catalog for RBAC matrix'

    def handle(self, *args, **options):
        created = seed_system_permissions()
        self.stdout.write(self.style.SUCCESS(f'Seeded permissions. New records: {created}'))
