from rest_framework import serializers
from .models import Expense , ExpenseCategory

class ExpenseSerializer(serializers.ModelSerializer):
    expense_category_name = serializers.CharField(source="expense_category.name", read_only=True, default=None)
    department_name = serializers.CharField(source="department.name", read_only=True, default=None)
    employee_name = serializers.CharField(source="employee.username", read_only=True, default=None)
    employee_email = serializers.CharField(source="employee.email", read_only=True, default=None)

    class Meta:
        model = Expense
        fields = [
            "id",
            "employee",
            "employee_name",
            "employee_email",
            "expense_category",
            "expense_category_name",
            "amount",
            "department",
            "department_name",
            "expense_date",
            "reason",
            "status"
        ]
        read_only_fields = ["id", "employee", "status"]

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = [
            "id",
            "name",
            "description"
        ]


