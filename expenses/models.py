from django.db import models
from core.models import Department
from django.conf import settings

# Create your models here.
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    class Status(models.TextChoices):
        APPROVED = "approved" , "Approved"
        REJECTED = "rejected" , "Rejected"
        PENDING = "pending" , "Pending"

    employee = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="expenses")
    expense_category = models.ForeignKey(to=ExpenseCategory, on_delete=models.SET_NULL , null=True , related_name="expenses")
    amount = models.DecimalField(max_digits=12 , decimal_places=2)
    department = models.ForeignKey(to=Department , on_delete=models.SET_NULL , null=True , related_name="expenses")
    expense_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10 , choices=Status.choices , default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.amount}"