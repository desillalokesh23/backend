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
        return Response(self._serialize(tenant, request))

    def patch(self, request):
        tenant = request.user.tenant
        if tenant.is_profile_locked:
            return Response(
                {'detail': 'Profile is under review. Editing is disabled until admin completes review.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = TenantProfileSerializer(
            tenant,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        try:
            TenantService.update_profile(tenant, serializer.validated_data, user=request.user)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        tenant.refresh_from_db()
        return Response(self._serialize(tenant, request))

    def _serialize(self, tenant, request):
        completed, missing = check_profile_completion(tenant)
        data = TenantProfileSerializer(tenant, context={'request': request}).data
        data['missing_profile_fields'] = missing
        data['profile_completed'] = completed
        data['is_profile_locked'] = tenant.is_profile_locked
        return data


class ProfileSubmitReviewView(APIView):
    permission_classes = [IsAuthenticatedTenantUser]

    def post(self, request):
        tenant = request.user.tenant
        try:
            TenantService.submit_profile_for_review(tenant)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        tenant.refresh_from_db()
        return Response(ProfileView()._serialize(tenant, request))
