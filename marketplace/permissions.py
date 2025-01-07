
from rest_framework import permissions



class IsClient(permissions.BasePermission):
    """
    Custom permission to only allow clients to post jobs.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and has the 'client' role
        return request.user and request.user.is_authenticated and request.user.usermodel.role == 'Client'
    
class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow clients to post jobs.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and has the 'client' role
        return request.user and request.user.is_authenticated and request.user.usermodel.role == 'Admin'