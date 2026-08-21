from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models import User
from . import serializers
from .models import Expense , ExpenseCategory
from .permissions import ExpensePermission , ExpenseCategoryPermission
from reimbursement.models import Reimbursement
from notifications.models import Notification
from notifications.services import create_notification
# Create your views here.

class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = serializers.ExpenseSerializer
    permission_classes = [ExpensePermission]

    def perform_create(self, serializer):
        user = self.request.user
        dept = serializer.validated_data.get('department') or user.department
        expense = serializer.save(employee=user, department=dept)
        
        manager = expense.employee.manager
        if manager:
            create_notification(
                user=manager , 
                notification_type= Notification.NotificationType.EXPENSE_SUBMITTED ,
                title= "New Expense submitted",
                message=(
                    f"{expense.employee.email} submitted"
                    f"an expense of {expense.amount}"
                )
            )

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

        with transaction.atomic():
            expense.status = Expense.Status.APPROVED
            expense.save()

            Reimbursement.objects.get_or_create(
                expense = expense,
                defaults={
                    "employee" : expense.employee,
                    "amount" : expense.amount,
                }
            )

        create_notification(
            user=expense.employee , 
            notification_type=(Notification.NotificationType.EXPENSE_APPROVED),
            title="Expnse Approved",
            message=(
                f"Your expense of ${expense.amount}"
                "has been approved."
            )
        )
        finance_managers = User.objects.filter(
            role = User.Role.FINANCE_MANAGER
        )
        for finance_manager in finance_managers:
            create_notification(
                user=finance_manager , 
                notification_type=(Notification.NotificationType.REIMBURSEMENT_CREATED),
                title="New Reimbursement",
                message=(
                    f"A reimbursement of ₹{expense.amount} "
                    "is ready for processing."
                )
            )
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
        create_notification(
            user=expense.employee , 
            notification_type=(Notification.NotificationType.EXPENSE_REJECTED),
            title="Expense Rejected",
            message=(
                f"Your expense of ₹{expense.amount} "
                "has been rejected"
            )
        )
        expense.status = Expense.Status.REJECTED
        expense.save()


        return Response({
            "message" : "Expense rejected successfully",
            "expense_id" : expense.id,
            "status": expense.status
        }, status=status.HTTP_200_OK)

class ExpenseCategoryViewSet(ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = serializers.ExpenseCategorySerializer
    permission_classes = [ExpenseCategoryPermission]
