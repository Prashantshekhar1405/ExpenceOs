from rest_framework import serializers
from .models import Reimbursement

class ReimbursementSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.username", read_only=True, default=None)
    employee_email = serializers.CharField(source="employee.email", read_only=True, default=None)
    department = serializers.SerializerMethodField()
    reason = serializers.CharField(source="expense.reason", read_only=True, default=None)
    category = serializers.SerializerMethodField()
    expense_date = serializers.DateField(source="expense.expense_date", read_only=True, default=None)
    receipt_url = serializers.SerializerMethodField()
    class Meta:
        model = Reimbursement
        fields = [
            "id",
            "expense",
            "employee",
            "employee_name",
            "employee_email",
            "department",
            "reason",
            "category",
            "expense_date",
            "receipt_url",
            "amount",
            "status",
            "processed_by",
            "processed_at",
            "transaction_reference",
            "failure_reason",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "employee",
            "expense",
            "amount",
            "status",
            "processed_by",
            "processed_at",
            "created_at",
            "updated_at",
        ]

    
    def get_department(self, obj):
        if obj.expense and obj.expense.department:
            return obj.expense.department.name
        if obj.employee and obj.employee.department:
            return obj.employee.department.name
        return None

    def get_category(self, obj):
        if obj.expense and obj.expense.expense_category:
            return obj.expense.expense_category.name
        return None

    def get_receipt_url(self, obj):
        if obj.expense:
            receipt = obj.expense.receipts.first()
            if receipt and receipt.file:
                request = self.context.get("request")
                if request:
                    return request.build_absolute_uri(receipt.file.url)
                return receipt.file.url
        return None