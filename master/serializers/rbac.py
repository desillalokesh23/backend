from rest_framework import serializers

from master.models.rbac import Role, RolePermission, SystemPermission
from master.models.user import User
from master.services.permission_service import get_role_permission_matrix, sync_role_permissions


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RolePermissionMatrixSerializer(serializers.Serializer):
    permissions = serializers.DictField(child=serializers.BooleanField())

    def update(self, instance, validated_data):
        sync_role_permissions(instance, validated_data['permissions'])
        return instance

    def to_representation(self, instance):
        return {'permissions': get_role_permission_matrix(instance)}


class SystemPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPermission
        fields = ['id', 'module', 'action', 'codename', 'label']


class TenantUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    full_name = serializers.SerializerMethodField()

    is_active = serializers.BooleanField(source='is_active_user')

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone_number',
            'role',
            'role_name',
            'branch',
            'branch_name',
            'is_active',
            'is_active_user',
            'is_tenant_admin',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined', 'role_name', 'branch_name', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.email

    def create(self, validated_data):
        tenant = self.context['tenant']
        email = validated_data.pop('email', None) or self.initial_data.get('email')
        password = self.initial_data.get('password', 'ChangeMe@123')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            tenant=tenant,
            **validated_data,
        )
        user.created_by = self.context['request'].user
        user.save()
        return user
