from rest_framework.permissions import BasePermission
from .models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.EMPLOYEE
        )
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.MANAGER
        )
class IsFinanceManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.FINANCE_MANAGER
        )
class IsAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET" , "HEAD" , "OPTIONS"]:
            return request.user.is_authenticated

        return(
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )
