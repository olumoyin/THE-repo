from rest_framework import permissions





class IsWispOperator(permissions.BasePermission):
    message = 'You are not a WISP Operator.'
    
    def has_permission(self, request, view):
        # Allow full access to admin users.
        if request.user.is_staff:   
            return True
        
        # Allow full access to wisp operators.
        if request.user.is_wisp_operator:
            return True

        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a resource object to edit it.
    Accessible to Admin users.
    """
    def has_object_permission(self, request, view, obj):

        # Allow full access to admin users.
        if request.user.is_staff:
            return True
        
        # Check if the object is the request user for cases where users are requesting profiles.
        if obj == request.user:
            return True
        
        # Check if the object has a 'user' attribute and if the request user is the owner.
        if hasattr(obj, "user") and obj.user == request.user:
            return True
        
        

        
        return False


