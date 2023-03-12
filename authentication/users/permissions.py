from rest_framework.permissions import BasePermission


class IsTeam(BasePermission):
    message = "User not a Team member."

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.user.is_team:
            return True
        return False


class IsFounder(BasePermission):
    message = "User not a company founder."

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.user.id_founder:
            return True
        return False


class IsLP(BasePermission):
    message = "User not a LP"
    
    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.user.is_partnership:
            return True
        return False
