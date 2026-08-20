from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Reimbursement
from .serializers import ReimbursementSerializer
from .permissions import ReimbursementPermission
from core.models import User
from notifications.services import create_notification
from notifications.models import Notification

# Create your views here.

class ReimbursementViewSet(ModelViewSet):
    queryset = Reimbursement.objects.all()
    serializer_class = ReimbursementSerializer
    permission_classes = [ReimbursementPermission]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            return Reimbursement.objects.all()

        if user.role == User.Role.EMPLOYEE:
            return Reimbursement.objects.filter(employee = user)

        if user.role == User.Role.FINANCE_MANAGER:
            return Reimbursement.objects.all()

        return Reimbursement.objects.none()

    @action(detail = True , methods=["post"])
    def process(self , request , pk = None):
        reimbursement = self.get_object()

        if reimbursement.status != Reimbursement.Status.PENDING:
            return Response({
                "detail" : (
                    "only pending reibursements can be processed"
                )
            }, status=status.HTTP_400_BAD_REQUEST)

        reimbursement.status = (Reimbursement.Status.PROCESSING)
        reimbursement.processed_by = request.user

        reimbursement.save(
            update_fields=[
                "status",
                "processed_by",
                "updated_at",
            ]
        )
        create_notification(
            user = reimbursement.employee,
            notification_type=(Notification.NotificationType.REIMBURSEMENT_PROCESSING),
            title="reimbursement processing",
            message=(
                f"Your reimbursement of ${reimbursement.amount}"
                "is under processing"
            )
        )
        return Response(ReimbursementSerializer(reimbursement).data)

    @action(detail=True , methods=["post"])
    def pay(self , request , pk = None):
        reimbursement = self.get_object()

        if reimbursement.status != Reimbursement.Status.PROCESSING:
            return Response({
                "detail" : (
                    "only processing reibursements can be payed"
                )
            }, status=status.HTTP_400_BAD_REQUEST)

        transaction_reference = request.data.get("transaction_reference")

        if not transaction_reference:
            return Response(
                {
                    "transaction_reference" : (
                        "Transaction_reference is required"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reimbursement.status = (Reimbursement.Status.PAID)
        reimbursement.transaction_reference = (transaction_reference)
        reimbursement.processed_at = timezone.now()
        reimbursement.save(
            update_fields = [
                "status",
                "transaction_reference",
                "processed_at",
                "updated_at",
            ]
        )
        expense = reimbursement.expense
        expense.status = Expense.Status.PAID
        expense.save(update_fields=["status", "updated_at"])
        
        create_notification(
            user = reimbursement.employee,
            notification_type=(Notification.NotificationType.REIMBURSEMENT_PAID),
            title="reimbursement payed",
            message=(
                f"Your reimbursement of ${reimbursement.amount}"
                "has been paid"
            )
        )
        return Response(ReimbursementSerializer(reimbursement).data)



    @action(detail=True , methods=["post"])
    def fail(self , request, pk=None):
        reimbursement = self.get_object()

        if reimbursement.status != Reimbursement.Status.PROCESSING:
            return Response({
                "detail" : (
                    "only processing reibursements can be failed"
                )
            }, status=status.HTTP_400_BAD_REQUEST)

        reason = request.data.get("failure_reason")
        if not reason :
            return Response(
                {
                    "failure reason":(
                        "failure reason is required"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reimbursement.status = Reimbursement.Status.FAILED
        reimbursement.failure_reason = reason
        reimbursement.save(
            update_fields=[
                "status",
                "failure_reason",
                "updated_at",
            ]
        )
        create_notification(
            user = reimbursement.employee,
            notification_type=(Notification.NotificationType.REIMBURSEMENT_FAILED),
            title="reimbursement failed",
            message=(
                f"Your reimbursement of ${reimbursement.amount}"
                "has failed"
            )
        )
        return Response(ReimbursementSerializer(reimbursement).data)