import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser , FormParser
from .models import Receipt
from .serializers import ReceiptSerializer
from .permissions import ReceiptPermission
from core.models import User
from expenses.models import Expense
from .services.ocr import extract_text
from .services.parser import parse_receipt
from notifications.services import create_notification
from notifications.models import Notification
# Create your views here.
logger = logging.getLogger(__name__)

class ReceiptViewSet(ModelViewSet):
    queryset = Receipt.objects.none()
    serializer_class = ReceiptSerializer
    permission_classes = [ReceiptPermission]
    parser_classes = [MultiPartParser , FormParser]



    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            return Receipt.objects.all()

        if user.role == User.Role.EMPLOYEE:
            return Receipt.objects.filter(
                expense__employee = user
            )
        if user.role == User.Role.MANAGER:
            return Receipt.objects.filter(
                expense__employee__manager = user
            )
        if user.role == User.Role.FINANCE_MANAGER:
            return Receipt.objects.filter(
                expense__status = Expense.Status.APPROVED
            )
        return Receipt.objects.none()

    def perform_create(self, serializer):
        receipt = serializer.save()
        try:
            receipt.ocr_status = Receipt.OCRStatus.PROCESSING
            receipt.save(update_fields = ["ocr_status"])

            text = extract_text(receipt.file.path)
            data = parse_receipt(text)
            receipt.raw_text = text
            receipt.merchant = data["merchant"]

            if data["receipt_amount"]:
                receipt.receipt_amount = data["receipt_amount"]

            if data["receipt_date"]:
                receipt.receipt_date = data["receipt_date"]
                
            if data["tax_amount"] is not None:
                receipt.tax_amount = data["tax_amount"]

            if data["invoice_number"]:
                receipt.invoice_number = data["invoice_number"]

            receipt.ocr_status = Receipt.OCRStatus.COMPLETED
            receipt.save()
            create_notification(
                user= receipt.expense.employee,
                notification_type=(Notification.NotificationType.OCR_COMPLETED),
                title="Receipt OCR completed",
                message=("your receipt has been processed successfully"),
            )
        except Exception:
            logger.exception("ocr failed for receipt %s", receipt.id)

            receipt.ocr_status = Receipt.OCRStatus.FAILED
            receipt.save(update_fields=["ocr_status"])
            create_notification(
                user= receipt.expense.employee,
                notification_type=(Notification.NotificationType.OCR_FAILED),
                title="Receipt OCR failed",
                message=("your receipt has failed to process"),
            )