from rest_framework.permissions import BasePermission

from apps.users.models import Profile


class IsClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        return hasattr(user, "profile") and user.profile.role == Profile.Type.CLIENT


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        return hasattr(user, "profile") and user.profile.role == Profile.Type.DOCTOR


class IsHospital(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        return hasattr(user, "profile") and user.profile.role == Profile.Type.HOSPITAL


class IsPharmacy(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        return hasattr(user, "profile") and user.profile.role == Profile.Type.PHARMACY


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
