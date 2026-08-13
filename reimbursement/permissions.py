from rest_framework.permissions import BasePermission
from core.models import User

class ReimbursementPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user = request.user

        if user.role == User.Role.ADMIN:
            return True

        if user.role == User.Role.EMPLOYEE:
            return view.action in [
                "list",
                "retrieve",
            ]
        if user.role == User.Role.FINANCE_MANAGER:
            return view.action in [
                "list",
                "retrieve",
                "process",
                "pay",
                "fail",
            ]

        return False