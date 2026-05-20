from rest_framework import viewsets

from master.permissions.base import IsAuthenticatedTenantUser


class TenantScopedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedTenantUser]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser and not user.tenant_id:
            return qs
        return qs.filter(tenant=user.tenant, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user,
            updated_by=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete()
