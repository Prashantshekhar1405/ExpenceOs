from rest_framework.permissions import BasePermission
from .models import Receipt
from core.models import User

class ReceiptPermission(BasePermission):
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
                "create",
                "destroy"
            ]

        if user.role == User.Role.MANAGER:
            return view.action in [
                "list",
                "retrieve"
            ]
        if user.role == User.Role.FINANCE_MANAGER:
            return view.action in [
                "list",
                "retrieve"
            ]

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == User.Role.ADMIN:
            return True

        if user.role == User.Role.EMPLOYEE:
            return obj.expense.employee == user

        if user.role == User.Role.MANAGER:
            return obj.expense.employee.manager == user

        if user.role == User.Role.FINANCE_MANAGER:
            return obj.expense.status == "APPROVED"

        return False