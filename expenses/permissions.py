from rest_framework.permissions import BasePermission
from core.models import User
from .models import Expense

class ExpensePermission(BasePermission):

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
                "update",
                "partial_update",
                "destroy",
            ]

        if user.role == User.Role.MANAGER:
            return view.action in [
                "list",
                "retrieve",
            ]

        if user.role == User.Role.FINANCE_MANAGER:
            return view.action in [
                "list",
                "retrieve",
            ]

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == User.Role.ADMIN:
            return True

        if user.role == User.Role.EMPLOYEE:

            if obj.employee != user:
                return False
            
            if view.action in ["update","partial_update","destroy"]:
                return obj.status == obj.Status.PENDING
            
            return True

        if user.role == User.Role.MANAGER:
            return obj.employee.manager == user

        if user.role == User.Role.FINANCE_MANAGER:
            return obj.status == obj.Status.APPROVED

        return False

