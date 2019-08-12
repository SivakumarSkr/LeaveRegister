from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserCreatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser

