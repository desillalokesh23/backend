from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from master.permissions.base import IsAuthenticatedTenantUser
from master.serializers.tenant import TenantProfileSerializer
from master.services.tenant_service import TenantService
from master.utils.profile import check_profile_completion


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedTenantUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        tenant = request.user.tenant
        check_profile_completion(tenant)
        return Response(TenantProfileSerializer(tenant, context={'request': request}).data)

    def patch(self, request):
        tenant = request.user.tenant
        serializer = TenantProfileSerializer(
            tenant,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        TenantService.update_profile(tenant, serializer.validated_data, user=request.user)
        tenant.refresh_from_db()
        completed, missing = check_profile_completion(tenant)
        data = TenantProfileSerializer(tenant, context={'request': request}).data
        data['missing_profile_fields'] = missing
        return Response(data, status=status.HTTP_200_OK)
