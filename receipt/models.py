from django.db import models
from expenses.models import Expense
# Create your models here.
class Receipt(models.Model):
    expense = models.ForeignKey(to=Expense , on_delete=models.CASCADE , related_name="receipts")
    file = models.FileField(upload_to="receipts/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt - {self.expense.id}"