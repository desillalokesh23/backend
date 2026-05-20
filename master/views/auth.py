from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from master.serializers.auth import AuthUserSerializer, LoginSerializer, SignupSerializer
from master.services.auth_service import AuthService
from master.utils.profile import check_profile_completion

User = get_user_model()


def build_auth_payload(user):
    refresh = RefreshToken.for_user(user)
    if user.tenant_id:
        refresh['tenant_id'] = str(user.tenant_id)
        refresh['tenant_status'] = user.tenant.status
    completed, _ = check_profile_completion(user.tenant) if user.tenant else (True, [])
    data = {
        'id': user.id,
        'email': user.email,
        'name': user.get_full_name() or user.email,
        'company': user.tenant.company_name if user.tenant else '',
        'role': user.role.name if user.role else '',
        'is_tenant_admin': user.is_tenant_admin,
        'tenant_id': user.tenant_id,
        'tenant_status': user.tenant.status if user.tenant else None,
        'profile_completed': user.tenant.profile_completed if user.tenant else True,
        'tenant_approved': user.tenant.is_approved if user.tenant else True,
        'profile_review_status': user.tenant.profile_review_status if user.tenant else None,
        'is_profile_locked': user.tenant.is_profile_locked if user.tenant else False,
    }
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': AuthUserSerializer(data).data,
    }


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            tenant, user = AuthService.register_tenant(**serializer.validated_data)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        payload = build_auth_payload(user)
        payload['message'] = (
            'Tenant registered successfully. Awaiting admin approval for full access.'
        )
        return Response(payload, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.authenticate_user(
            serializer.validated_data['email_id'],
            serializer.validated_data['password'],
        )
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(build_auth_payload(user))


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        completed, missing = (
            check_profile_completion(user.tenant) if user.tenant else (True, [])
        )
        data = {
            'id': user.id,
            'email': user.email,
            'name': user.get_full_name() or user.email,
            'company': user.tenant.company_name if user.tenant else '',
            'role': user.role.name if user.role else '',
            'is_tenant_admin': user.is_tenant_admin,
            'tenant_id': user.tenant_id,
            'tenant_status': user.tenant.status if user.tenant else None,
            'profile_completed': completed,
            'tenant_approved': user.tenant.is_approved if user.tenant else True,
            'profile_review_status': user.tenant.profile_review_status if user.tenant else None,
            'is_profile_locked': user.tenant.is_profile_locked if user.tenant else False,
            'missing_profile_fields': missing,
        }
        return Response(AuthUserSerializer(data).data | {'missing_profile_fields': missing})
