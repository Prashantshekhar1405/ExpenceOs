from django.db import models
from expenses.models import Expense
from core.models import User
# Create your models here.

class Reimbursement(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending" , "Pending"
        PROCESSING = "processing" , "Processing"
        PAID = "paid" , "Paid"
        FAILED = "failed" , "Failed"

    expense = models.OneToOneField(to=Expense , on_delete=models.CASCADE , related_name="reimbursement")
    employee = models.ForeignKey(to=User ,   on_delete=models.CASCADE , related_name="reimbursement")
    amount = models.DecimalField(max_digits=12 , decimal_places=2)
    status = models.CharField(max_length=20 , choices=Status.choices , default=Status.PENDING)
    processed_by = models.ForeignKey(to=User , on_delete=models.SET_NULL , null=True , blank=True , related_name="processed_reimbursement")
    processed_at = models.DateTimeField(null=True , blank=True)
    transaction_reference = models.CharField(max_length=255 , blank=True)
    failure_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reimbursement - Expense {self.expense.id}"