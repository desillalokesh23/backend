from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from master.views.auth import LoginView, MeView, SignupView
from master.views.masters import (
    BranchViewSet,
    DriverViewSet,
    PackageTypeViewSet,
    RouteViewSet,
    ServiceTypeViewSet,
    VehicleTypeViewSet,
    WarehouseViewSet,
)
from master.views.profile import ProfileSubmitReviewView, ProfileView
from master.views.rbac import RoleViewSet, SystemPermissionViewSet, TenantUserViewSet

router = DefaultRouter()
router.register('masters/roles', RoleViewSet, basename='role')
router.register('masters/users', TenantUserViewSet, basename='tenant-user')
router.register('masters/permissions', SystemPermissionViewSet, basename='system-permission')
router.register('masters/branches', BranchViewSet, basename='branch')
router.register('masters/warehouses', WarehouseViewSet, basename='warehouse')
router.register('masters/routes', RouteViewSet, basename='route')
router.register('masters/service-types', ServiceTypeViewSet, basename='service-type')
router.register('masters/package-types', PackageTypeViewSet, basename='package-type')
router.register('masters/vehicle-types', VehicleTypeViewSet, basename='vehicle-type')
router.register('masters/drivers', DriverViewSet, basename='driver')

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/submit-review/', ProfileSubmitReviewView.as_view(), name='profile-submit-review'),
    path('', include(router.urls)),
]
