from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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

    @action(detail=True , methods=["post"])
    def approve(self , request ,pk = None):
        expense = self.get_object()

        if expense.status != Expense.Status.PENDING:
            return Response({
                "message" : "only pending expense can be approved"
            } , status=status.HTTP_400_BAD_REQUEST)
        
        expense.status = Expense.Status.APPROVED
        expense.save()
        return Response({
            "message" : "Expense approved successfully",
            "expense_id" : expense.id,
            "status" : expense.status
        },status=status.HTTP_200_OK)


    @action(detail=True , methods=["post"])
    def reject(self , request , pk = None):
        expense = self.get_object()

        if expense.status != Expense.Status.PENDING:
            return Response({
                "message" : "only pending expenses can be rejected"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        expense.status = Expense.Status.REJECTED
        expense.save()

        return Response({
            "message" : "Expense rejected successfully",
            "expense_id" : expense.id,
            "status": expense.status
        }, status=status.HTTP_200_OK)

