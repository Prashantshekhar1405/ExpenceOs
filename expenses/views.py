from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from core.models import User
from . import serializers
from .models import Expense
from .permissions import ExpensePermission
# Create your views here.
class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = serializers.ExpenseSerializer
    permission_classes = [ExpensePermission]

    def perform_create(self, serializer):
        serializer.save(employee = self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.EMPLOYEE:
            return Expense.objects.filter(employee = user)

        if user.role == User.Role.MANAGER:
            return Expense.objects.filter(employee__manager = user)

        if user.role == User.Role.FINANCE_MANAGER:
            return Expense.objects.filter(
                status = Expense.Status.APPROVED
            )
        if user.role == User.Role.ADMIN:
            return Expense.objects.all()

        return Expense.objects.none()

