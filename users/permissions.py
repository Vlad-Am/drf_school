from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверка на модератора"""

    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moder').exists()


class IsOwner(permissions.BasePermission):
    """ Проверка на владельца """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if obj.owner == request.user:
            return True
        return False
