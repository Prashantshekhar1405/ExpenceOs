from django.contrib import admin
from .models import ExpenseCategory , Expense
# Register your models here.
@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("id" , "name")

@admin.register(Expense)
class Expense(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
        "expense_category",
        "amount",
        "department",
        "status",
        "reason",
        "expense_date"
    )

    list_filter = (
        "status" ,
        "department",
        "expense_category"
    )
    search_fields = (
        "employee__email",
        "employee__email_id",
        "reason",
    )