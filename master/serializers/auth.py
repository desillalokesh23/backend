from rest_framework import serializers

from master.validators.auth import validate_signup_password


class SignupSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    company_name = serializers.CharField(max_length=255)
    contact_person = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)

    def validate_password(self, value):
        validate_signup_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    email_id = serializers.CharField()
    password = serializers.CharField(write_only=True)


class AuthUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    name = serializers.CharField()
    company = serializers.CharField()
    role = serializers.CharField(allow_blank=True)
    is_tenant_admin = serializers.BooleanField()
    tenant_id = serializers.UUIDField(allow_null=True)
    tenant_status = serializers.CharField(allow_null=True)
    profile_completed = serializers.BooleanField()
    tenant_approved = serializers.BooleanField()
    profile_review_status = serializers.CharField(allow_null=True, required=False)
    is_profile_locked = serializers.BooleanField(required=False)
