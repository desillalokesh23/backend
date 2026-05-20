from django.contrib.auth import get_user_model
from rest_framework import serializers

from master.models.rbac import Role, SystemPermission
from master.services.permission_service import get_role_permission_matrix, sync_role_permissions

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'order_id', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_order_id(self, value):
        tenant = self.context['request'].user.tenant
        qs = Role.objects.filter(tenant=tenant, order_id=value, is_deleted=False)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Order ID must be unique within your organization.')
        return value

    def validate_name(self, value):
        tenant = self.context['request'].user.tenant
        qs = Role.objects.filter(tenant=tenant, name__iexact=value.strip(), is_deleted=False)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A role with this name already exists.')
        return value.strip()


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


class TenantUserListSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(source='is_active_user')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'phone_number',
            'designation',
            'role',
            'role_name',
            'is_active',
            'date_joined',
        ]
        read_only_fields = fields

    def get_username(self, obj):
        return '***'

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.email


class TenantUserDetailSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(source='is_active_user')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'designation',
            'role',
            'role_name',
            'is_active',
            'is_active_user',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined', 'role_name', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.email


class TenantUserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    designation = serializers.CharField(max_length=150, required=False, allow_blank=True)
    role = serializers.UUIDField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate_role(self, value):
        if value in (None, ''):
            return None
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        tenant = self.context['request'].user.tenant
        username = attrs['username'].strip()
        email = attrs['email'].lower().strip()
        attrs['email'] = email
        attrs['username'] = username
        if User.objects.filter(tenant=tenant, username__iexact=username).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        tenant = self.context['request'].user.tenant
        role_id = validated_data.pop('role', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            tenant=tenant,
            is_active=True,
            is_active_user=True,
            **validated_data,
        )
        if role_id:
            user.role_id = role_id
            user.save(update_fields=['role'])
        return user


class TenantUserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'designation',
            'role',
            'is_active_user',
            'password',
            'confirm_password',
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm = attrs.get('confirm_password')
        if password or confirm:
            if password != confirm:
                raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        else:
            attrs.pop('password', None)
            attrs.pop('confirm_password', None)
        tenant = self.context['request'].user.tenant
        username = attrs.get('username')
        if username:
            qs = User.objects.filter(tenant=tenant, username__iexact=username.strip())
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'username': 'Username already exists.'})
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        if 'is_active_user' in validated_data:
            validated_data['is_active'] = validated_data['is_active_user']
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# Backward-compatible alias for viewset default
TenantUserSerializer = TenantUserListSerializer
