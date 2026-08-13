from django.db import models
from expenses.models import Expense
# Create your models here.
class Receipt(models.Model):
    class OCRStatus(models.TextChoices):
        PENDING = "pending" , "Pending"
        PROCESSING = "processing" , "Processing"
        COMPLETED = "completed" , "Completed"
        FAILED = "failed" , "Failed"

    expense = models.ForeignKey(to=Expense , on_delete=models.CASCADE , related_name="receipts")
    file = models.FileField(upload_to="receipts/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ocr_status = models.CharField(max_length=20 , choices=OCRStatus.choices , default=OCRStatus.PENDING)
    merchant = models.CharField(max_length=255 , blank=True)
    receipt_amount = models.DecimalField(max_digits=10 , decimal_places=2 , null=True , blank=True)
    receipt_date = models.DateField(null=True , blank=True)
    tax_amount = models.DecimalField(max_digits=12 , decimal_places=2 , null=True , blank=True)
    invoice_number = models.CharField(max_length=100 , null=True , blank=True)
    raw_text = models.TextField(blank=True)

    def __str__(self):
        return f"Receipt - {self.expense.id}"