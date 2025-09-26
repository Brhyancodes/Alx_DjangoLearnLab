# api/permissions.py

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only authors to edit their own books.
    Read permissions are allowed to any request,
    Write permissions are only allowed to authenticated users who are the author.
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to access the view.
        """
        # Read permissions for all users (authenticated or not)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to access a specific object.
        """
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for authenticated users
        if not request.user or not request.user.is_authenticated:
            return False

        # For this example, any authenticated user can modify any book
        # In a real application, you might want to check if the user
        # is the author of the book or has specific roles
        return True


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only staff members to create, update, or delete.
    Read permissions are allowed to any request.
    """

    def has_permission(self, request, view):
        """
        Check if user has permission to access the view.
        """
        # Read permissions for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for staff users
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to edit it.
    Assumes the model has an 'owner' field.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to access a specific object.
        """
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only to the owner of the object
        # Note: This assumes your model has an 'owner' field
        # Since our Book model doesn't have an owner field,
        # this is more of an example for future use
        return hasattr(obj, "owner") and obj.owner == request.user
