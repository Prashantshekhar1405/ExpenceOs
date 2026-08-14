from django.db import models
from core.models import User
# Create your models here.

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        EXPENSE_SUBMITTED = "expense_submitted", "Expense Submitted"
        EXPENSE_APPROVED = "expense_approved", "Expense Approved"
        EXPENSE_REJECTED = "expense_rejected", "Expense Rejected"

        OCR_COMPLETED = "ocr_completed", "OCR Completed"
        OCR_FAILED = "ocr_failed", "OCR Failed"

        REIMBURSEMENT_CREATED = ("reimbursement_created","Reimbursement Created")
        REIMBURSEMENT_PROCESSING = ("reimbursement_processing","Reimbursement Processing")
        REIMBURSEMENT_PAID = ("reimbursement_paid","Reimbursement Paid")
        REIMBURSEMENT_FAILED = ("reimbursement_failed","Reimbursement Failed")

        BUDGET_WARNING = "budget_warning", "Budget Warning"

        SYSTEM = "system", "System"

    user = models.ForeignKey(to=User , on_delete=models.CASCADE , related_name="notifications")
    notification_type = models.CharField(max_length=50 , choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.title}"