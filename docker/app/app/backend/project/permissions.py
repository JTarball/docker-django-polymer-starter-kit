'''
    project.permissions
    ===================

    Project / Global Custom Permissions for REST API
'''
import logging

from rest_framework import permissions

logger = logging.getLogger('test_logger')

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            logger.info("%s" % request.method)
            return True

        # Write permissions are only allowed to the owner of the snippet
        return request.user.is_staff or request.user.is_superuser
