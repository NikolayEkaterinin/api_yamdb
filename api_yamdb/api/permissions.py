from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminUserOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or super().has_permission(request, view))


class IsAuthorAdminSuperuserOrReadOnly(permissions.BasePermission):
    message = (
        'Проверка пользователя является ли он администрацией'
        'или автором объекта, иначе только режим чтения'
    )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user))
