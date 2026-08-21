from rest_framework import serializers
from .models import Expense , ExpenseCategory

class ExpenseSerializer(serializers.ModelSerializer):
    expense_category_name = serializers.CharField(source="expense_category.name", read_only=True, default=None)
    department_name = serializers.SerializerMethodField()
    employee_name = serializers.CharField(source="employee.username", read_only=True, default=None)
    employee_email = serializers.CharField(source="employee.email", read_only=True, default=None)
    receipt_url = serializers.SerializerMethodField()
    receipt_name = serializers.SerializerMethodField()

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
            "status",
            "receipt_url",
            "receipt_name"
        ]
        read_only_fields = ["id", "employee", "status" , "receipt_url", "receipt_name"]

    def get_department_name(self, obj):
        if obj.department:
            return obj.department.name
        if obj.employee and obj.employee.department:
            return obj.employee.department.name
        return None

    def get_receipt_url(self, obj):
        receipt = obj.receipts.first()
        if receipt and receipt.file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(receipt.file.url)
            return receipt.file.url
        return None

    def get_receipt_name(self, obj):
        receipt = obj.receipts.first()
        if receipt and receipt.file:
            return receipt.file.name.split("/")[-1]
        return None


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = [
            "id",
            "name",
            "description"
        ]


