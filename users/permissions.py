from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin()

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_admin() or request.user.is_manager())

class IsAssigneeOrReadOnly(permissions.BasePermission):
    """
    Assignee can edit the task, managers/admins can create/update/delete, others read-only.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) allowed to everyone authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admins and managers can modify any task
        if request.user.is_admin() or request.user.is_manager():
            return True
        # Otherwise only assignee may update status/fields
        return obj.assignee == request.user