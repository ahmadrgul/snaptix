from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
        # staff can do anything
            return True
        
        if request.method in SAFE_METHODS:
        # read permissions are allowed to everyone
            return True
        
        # write permissions are only allowed to the assoicated organizer
        return user.is_authenticated and obj.organizer == user