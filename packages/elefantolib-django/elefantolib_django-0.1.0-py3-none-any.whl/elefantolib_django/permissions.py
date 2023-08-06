from rest_framework import permissions


class DenyAll(permissions.BasePermission):

    def has_permission(self, request, view):
        return False


class AllowAny(permissions.AllowAny):

    def has_permission(self, request, view):
        return request.pfm.user


class IsAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return request.pfm.user.is_authenticated()
